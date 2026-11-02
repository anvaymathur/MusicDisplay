# MusicDisplay
A TFT touch screen music display that changes over bluetooth. Displays the current music playing and time.

## Description

The reason I wanted to build this is because, often when I listen to music while studying. If i ever want to change the 
music or adjust the volume, I get distracted looking at my phone. I also don't have headphones which can switch the music from
itself. So I wanted something where I can control the music and look at time and only important stuff, but I can't get distracted from something else.

## Features

* 3D Printed Case (TODO)
* TFT LCD Touch Screen for controls
* Interact with spotify over bluetooth
* EC11 Rorary Encoder for controlling volume
* USB-C connection for

## PCB

Custom PCB made in KiCad. Footprint for the ESP32 was built entirely by claude.

![Schematic_Final.png](assets/FinishedSchematic.png)
![PCB_Final_Full.png](assets/FinishedPCB.png)
![PCB_3D_TOP.png](assets/3DFront.png)
![PCB_3D_BOTTOM.png](assets/3DBack.png)

## Firmware

There is custom firmware for showing the current song, title, and artist. It shows the app name being used (ie. spotify) and time. Allows you to play and pause. It also shows the album picture and volume bar. It uses the knob 
to change the volumel, mute and unmute, and update the brightness of the screen. 

## BOM

| Item  | Description | # of Sets | #Pcs / Set | Price / Set (USD) | Item Total Price + Tax & Shipping (USD)| Supplier | URL |
| ----- | ----------- | --------- | ---------- | ----------------- | -------------------------------------- | -------- | -------| 
|Megaboard PCB Printing with JLCPCB | PCB | 1 | 5 | $5.20 | $12.11 | JLC PCB | https://kommodo.ai/iMpm5V022tOTxhFTwnaLW |
| SPI TFT LCD Touch Panel - 2.8" with Touch | TFT Touch Screen | 1 | 1 | $8.55 | $8.55 | AliExpress | https://www.aliexpress.com/item/32847628219.html?spm=a2g0o.productlist.main.2.33cf77b1gnrpY5&algo_pvid=0509a18b-44e0-4fb3-b00a-1c4f3944f9be&algo_exp_id=0509a18b-44e0-4fb3-b00a-1c4f3944f9be-1&pdp_ext_f=%7B%22order%22%3A%223864%22%2C%22spu_best_type%22%3A%22price%22%2C%22eval%22%3A%221%22%2C%22fromPage%22%3A%22search%22%7D&pdp_npi=6%40dis%21USD%217.65%217.65%21%21%217.65%217.65%21%402103128917932955914718541e0eb0%2112000033182735606%21sea%21CA%218292344353%21X%211%210%21n_tag%3A-29911%3Bd%3Adfeb2caa%3Bm03_new_user%3A-29895&curPageLogUid=1SAzQbczehUA&utparam-url=scene%3Asearch%7Cquery_from%3A%7Cx_object_id%3A32847628219%7C_p_origin_prod%3A |
| ESP32-S3 Supermini dev board | Microcontroller  | 1 | 1 | $3.49 | $3.49 | AliExpress | https://www.aliexpress.com/item/1005007523993589.html?spm=a2g0o.productlist.main.3.5b3b4090pWHUtf&algo_pvid=55434281-e44d-4b08-b09e-9082ebce36cd&algo_exp_id=55434281-e44d-4b08-b09e-9082ebce36cd-2&pdp_ext_f=%7B%22order%22%3A%22402%22%2C%22eval%22%3A%221%22%2C%22fromPage%22%3A%22search%22%7D&pdp_npi=6%40dis%21USD%213.49%213.49%21%21%213.49%213.49%21%402101f43b17933647155257133e0e12%2112000044263237981%21sea%21CA%218292344353%21X%211%210%21n_tag%3A-29911%3Bd%3Adfeb2caa%3Bm03_new_user%3A-29895&curPageLogUid=VGpB42wyyM2v&utparam-url=scene%3Asearch%7Cquery_from%3A%7Cx_object_id%3A1005007523993589%7C_p_origin_prod%3A |
| 360 Degree Rotary Encoder EC11 | Rotary Encoder | 1 | 3 | $1.19 | $1.19 | AliExpress | https://www.aliexpress.com/item/1005007644083514.html?spm=a2g0o.productlist.main.1.414b17573arSFE&algo_pvid=43460615-9ee4-41ed-ac14-7b29d6321f60&algo_exp_id=43460615-9ee4-41ed-ac14-7b29d6321f60-0&pdp_ext_f=%7B%22order%22%3A%224875%22%2C%22spu_best_type%22%3A%22price%22%2C%22eval%22%3A%221%22%2C%22fromPage%22%3A%22search%22%7D&pdp_npi=6%40dis%21USD%211.82%211.82%21%21%211.82%211.82%21%402101ca8b17933654439705871e0e50%2112000041630839409%21sea%21CA%218292344353%21X%211%210%21n_tag%3A-29911%3Bd%3Adfeb2caa%3Bm03_new_user%3A-29895&curPageLogUid=m3IskyDbyq9m&utparam-url=scene%3Asearch%7Cquery_from%3A%7Cx_object_id%3A1005007644083514%7C_p_origin_prod%3A |       |
| **Grand Total**: | | | | | $25.34|    

## Thank You