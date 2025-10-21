# 06016423 INFRASTRUCTURE PROGRAMMABILITY AND AUTOMATION (1/2025)

## ข้อมูลสถานศึกษา
**สถานศึกษา:** สถาบันเทคโนโลยีพระจอมเกล้าเจ้าคุณทหารลาดกระบัง  
**คณะ:** เทคโนโลยีสารสนเทศ  
**สาขา:** เทคโนโลยีสารสนเทศ  
**แขนง:** โครงสร้างพื้นฐานเทคโนโลยีสารสนเทศ

## ข้อมูลนักศึกษา
**ชื่อ-นามสกุล:** นายธันยา วรมงคล  
**รหัสนักศึกษา:** 66070091

## คำแนะนำสภาพแวดล้อม
- แนะนำให้ใช้งานบน Linux (Ubuntu 24.04 LTS)
- Python ที่ใช้ทดสอบ: 3.12.3

## สิ่งที่ต้องติดตั้งก่อนใช้งาน
ติดตั้งแพ็กเกจระบบ (Ubuntu 24.04):
```bash
sudo apt update
sudo apt install -y git-all python3.12 python3.12-venv python3-pip ssh
```
หมายเหตุเพิ่มเติม:
- ปรับค่า IP/Username/Password ของเราเตอร์ได้ในไฟล์:
  - netmiko_final.py, restconf_final.py, ansible_final.py

## การติดตั้งและเตรียมใช้งาน
1) โคลนโปรเจกต์
```bash
git clone https://github.com/kuro-kano/IPA2024-Final.git
cd IPA2024-Final
```
2) สร้าง virtual environment และติดตั้ง dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## การตั้งค่าไฟล์ .env
1) คัดลอกไฟล์ตัวอย่างและแก้ไขค่า
```bash
cp .env.example .env
```
2) แก้ไฟล์ .env ให้กำหนดค่า:
- ACCESS_TOKEN = WEBEX_ACCESS_TOKEN ของคุณ
- ROOM_ID = WEBEX_ROOM_ID ที่ต้องการให้บอทอ่าน/ตอบกลับ

ตัวอย่างในไฟล์ .env:
```
ACCESS_TOKEN="xxxx-your-webex-personal-access-token-xxxx"
ROOM_ID="yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
```
แหล่งอ้างอิง:
- WEBEX_ACCESS_TOKEN: https://developer.webex.com/docs/getting-your-personal-access-token
- WEBEX_ROOM_ID: https://developer.webex.com/messaging/docs/api/v1/rooms/list-rooms

## วิธีการรัน
ภายใน virtual environment:
```bash
python ipa2024_final.py
```
หยุดโปรแกรมด้วย Ctrl+C

## การใช้งานคำสั่งใน Webex
พิมพ์ในห้อง Webex: "/66070091 <command>" โดยมีคำสั่งดังนี้:
- `create` : สร้าง Interface Loopback66070091 ผ่าน RESTCONF พร้อมกำหนด IP "172.0.91.1/24"
- `delete` : ลบ Interface Loopback66070091 ผ่าน RESTCONF
- `enable` : เปิดใช้งาน Interface Loopback66070091 (admin up) ผ่าน RESTCONF
- `disable` : ปิดใช้งาน Interface Loopback66070091 (admin down) ผ่าน RESTCONF
- `status` : ตรวจสอบสถานะของ Loopback66070091 ผ่าน RESTCONF
- `gigabit_status` : ดึงสถานะ interfaces ที่เป็น GigabitEthernet ทั้งหมดผ่าน netmiko
- `showrun` : รัน Ansible playbook เพื่อดึง show running-config แล้วอัปโหลดไฟล์ show_run_66070091_CSR1kv.txt กลับไปที่ห้อง Webex

หมายเหตุ:
- คำสั่ง showrun ต้องมี ansible ติดตั้งและไฟล์ playbook อยู่ที่ ansible/playbook_showrun.yaml
- ตรวจสอบว่า SSH ทำงานอยู่หรือไม่ โดยรัน `sudo service ssh status` หรือ `sudo systemctl status ssh` — หากสถานะเป็น inactive ให้รัน `sudo service ssh restart` หรือ `sudo systemctl restart ssh`
- หากเชื่อมต่ออุปกรณ์จริง ตรวจสอบให้แน่ใจว่าคอนฟิก RESTCONF/SSH ของอุปกรณ์เปิดใช้งานและ IP/รหัสผ่านถูกต้อง

