import os, grp, subprocess

USER_USER = os.getlogin()
USER_GROUP = grp.getgrnam(USER_USER).gr_name

os.system("clear")
print("Linux hosting panel managerga Hush kelibsiz")

def list_domains(file_path="/etc/hosts"):
    try:
        domains = []
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip() and not line.strip().startswith("#"):
                    parts = line.split()
                    if len(parts) > 1 and parts[0].count('.') == 3:
                        domains.extend(parts[1:])
        return True, domains
    except Exception as e:
        return False, str(e)

def add_hostname(domain, ip="127.0.0.1"):
    try:
        with open("/etc/hosts", 'r+') as file:
            hosts = file.read()
            lines = hosts.split("\n")
            for i, line in enumerate(lines):
                if ip in line:
                    if domain in line: return "⁕ Domain avval qo'shilgan"
                    lines[i] = f"{line} {domain}"
            newhosts = "\n".join(lines)
            with open("/etc/hosts", "w+") as fl:
                fl.write(newhosts)

        os.system("sudo systemctl restart systemd-resolved")
        return "⁕ Muvaffaqiyatli qo'shildi"
    except Exception as e:
        return "᳁ Xatolik: " + str(e)


def remove_hostname(domain, ip="127.0.0.1"):
    try:
        with open("/etc/hosts", 'r+') as file:
            hosts = file.read()
            lines = hosts.split("\n")
            for i, line in enumerate(lines):
                if ip in line:
                    if not (domain in line): return "⁕ Domain avval qo'shilmagan"
                    lined = line.replace(domain, '')
                    lines[i] = f"{lined}"
            newhosts = "\n".join(lines)
            with open("/etc/hosts", "w+") as fl:
                fl.write(newhosts)

        os.system("sudo systemctl restart systemd-resolved")
        return "⁕ Muvaffaqiyatli domain o'chirib tashlandi"
    except Exception as e:
        return "᳁ Xatolik: " + str(e)
    
    
def main():
    print("""Quyidagi buyruqlardan foydalaning:
        [0]. Domainlar ro'yhati
        [1]. Domain qo'shish
        [2]. Apache2 ga ulash  
        [3]. Apache2 dan uzish  
        [4]. Domain o'chirish
        
        [5]. Papkani ochish
        """)

    com = input("Command: ").strip()

    if com == '0':
        list_d = list_domains()
        if list_d[0]:
            print()
            print("⁕ Mavjud domenlar ro'yhati:")
            for domain in list_d[1]:
                print("  ", domain)
        else:
            print()
            print("᳁ Xatolik: " + str(list_d[1]))

    elif com == '1':
        domain = input("Yangi qo'shmoqchi bo'lgan domain nomini kiriting:\n-> ").strip()
        if domain != '':
            check_d = input(f"{domain} domainini qo'shishga ishonchingiz komilmi? [HA][YO'Q]\n-> ").strip()
            if check_d != '':
                print()
                print(add_hostname(domain))

    elif com == '2':
        try:
            domain = input("Domain nomini kiriting:\n-> ").strip()
            if domain != '':
                check_d = input(f"Apachega {domain} domainini qo'shish davom ettirilsinmi? [HA][YO'Q]\n-> ").strip()
                if check_d.lower() == 'ha':
                    os.mkdir(f"/var/www/{domain}", 0o755)
                    
                    os.system(f"sudo chown -R {USER_USER}:{USER_GROUP} /var/www/{domain}")
                    os.system(f"sudo chmod -R 755 /var/www/{domain}/")
                    
                    with open(f"/var/www/{domain}/index.html", "w+") as file:
                        file.write("<h1>SAYT ISHLAYAPTI</h1>")
                        
                    os.system(f"sudo chmod -R 755 /var/www/{domain}/*")
                    os.system(f"sudo chown -R {USER_USER}:{USER_GROUP} /var/www/{domain}")
                    with open(f"/etc/apache2/sites-available/{domain}.conf", "w+") as file:
                        file.write(f"""
    <VirtualHost *:80>
        ServerAdmin webmaster@{domain}
        ServerName {domain}
        ServerAlias www.{domain}
        DocumentRoot /var/www/{domain}

        ErrorLog ${{APACHE_LOG_DIR}}/error.log
        CustomLog ${{APACHE_LOG_DIR}}/access.log combined
    </VirtualHost>
                """)
                    os.system(f"sudo a2ensite {domain}.conf")
                    os.system("sudo systemctl restart apache2")
                    print()
                    print("⁕ Muvaffaqiyatli qo'shildi")
        except Exception as e:
            print("Xatolik: ", str(e))

    elif com == "3":
        try:
            domain = input("Domain nomini kiriting: ").strip()
            if domain != '':
                check_d = input(f"{domain} domainini apachedan uzmoqchimisiz? [HA][YO'Q]\n-> ").strip()
                if check_d != '':
                    os.system(f"sudo a2dissite {domain}.conf")
                    os.system(f"sudo rm /etc/apache2/sites-available/{domain}.conf")
                    os.system(f"sudo rm -r /var/www/{domain}")
                    os.system(f"sudo systemctl restart apache2")
                    print("⁕ Muvaffaqiyatli apache2 dan uzildi")
        except Exception as e:
            print("Xatolik:", str(e))

    elif com == "4":
        domain = input("Domain nomini kiriting:\n-> ").strip()
        if domain != '':
            check_d = input(f"{domain} domainini o'chirib tashlashga ishonchingiz komilmi? [HA][YO'Q]\n-> ").strip()
            if check_d != '':
                print()
                print(remove_hostname(domain))
                print("Domen 1 daqiqada DNS dan uziladi")
                
    elif com == "5":
        with open('/dev/null', 'w') as devnull:
            subprocess.Popen(['xdg-open', "/var/www"], stdout=devnull, stderr=subprocess.STDOUT)
        os.system("clear")

    else:
        os.system("clear")
        
    print()
    return

while True:
    main()
