# Module imports
import click, random, os, ctypes, subprocess, platform, psutil, webbrowser, urllib.request, win10toast, time

# Variables
chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
chrome_path_ing = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe -incognito %s"
toast = win10toast.ToastNotifier()

# Functions
def convertTime(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%d:%02d:%02d" % (hours, minutes, seconds)

# Group setups
@click.group()
def main():
    pass

@main.group()
def security():
    pass

@main.group()
def administrator():
    if not bool(ctypes.windll.shell32.IsUserAnAdmin()):
        click.echo("Please run this command with administrator rights. \n\033[1;31;40mAccess is denied. \033[0;37;40m\n")
        click.pause()
        exit()

@main.group()
def info():
    pass

@main.group()
def utilities():
    pass

# Security commands
@security.command(name="genpin")
@click.option("--length", "-l", default=8)
def genpin(length):
    rngnum = "1" + ("0" * (int(length) - 1))
    rn = random.randrange(0, int(rngnum))
    strrn = (length - len(str(rn))) * "0" + (str(rn))
    click.echo(strrn)

@security.command()
@click.option("--confirm", "-c", default="False")
def shutdown(confirm):
    if confirm == "True":
        click.echo("Shutdown will start in 12 seconds\n")
        os.system("shutdown -s -t 12 -c \"Shutdown called by cpbs\"")
    else:
        click.echo("Shutdown did not start. Add \"--confirm True\" option to start shutdown. \n")
        os.system("shutdown -a")

# Administrator commands
@administrator.command()
@click.argument("appname")
def killapp(appname):
    os.system(f"taskkill /f /im {appname}")

@administrator.command()
def opensecapp():
    click.echo("\033[1;33;40mOpening security apps...\033[0;37;40m")
    subprocess.Popen(["taskmgr"])
    subprocess.Popen(["regedit"])
    subprocess.Popen(["control"])

@administrator.command()
@click.argument("filename")
def filefullctrl(filename):
    os.system(f"takeown /f {filename}")
    os.system(f"icacls {filename} /grant {os.getlogin()}:(F,MA)")
    click.echo("Done. ")

@administrator.command()
@click.argument("foldername")
def dirfullctrl(foldername):
    os.system(f"takeown /f {foldername} /r /d y")
    os.system(f"icacls {foldername} /grant {os.getlogin()}:(F,MA)")
    click.echo("Done. ")

# Info commands
@info.command()
def system():
    prss = platform.processor()
    pltfrm = platform.platform()
    click.echo(f"\nPlatform: {pltfrm},\nProcessor: {prss}\n")

@info.command()
def cpbs():
    click.echo("Copyright 2021. codingPro01. All rights reserved. \n\033[1;33;40m  codingPro01 Basic Services - cli\n    Version: b 0.1.0\n    First made: Sep 2021, codingPro01.\n\033[1;32;40m    Ready to use. \033[0;37;40m")

@info.command()
def syshardstt():
    click.echo("Battery: ")
    batteryinfo = psutil.sensors_battery()
    plugged = batteryinfo.power_plugged
    percent = str(batteryinfo.percent) + "%"
    timeleft = "Power plugged in. "
    if not plugged:
        timeleft = convertTime(batteryinfo.secsleft)
    click.echo(f"  Percentage: {percent}\n  Power plugged: {str(plugged)}\n  Time left: {timeleft}")

# Utilities commands
@utilities.command()
@click.argument("url")
@click.option("--ig", "-i", default="False")
def openweb(url, ig):
    if ig == "True":
        webbrowser.get(chrome_path_ing).open(url)
    else:
        webbrowser.get(chrome_path).open(url)
    if "://" not in url:
        url = "https://" + url
    else:
        pass
    click.echo(f"Result code: {str(urllib.request.urlopen(url).getcode())}")

@utilities.command()
def afk():
    toast.show_toast("AFK Notification", "AFK Started", "app.ico", 4, True)
    time.sleep(4.2)
    ctypes.windll.user32.LockWorkStation()
    toast.show_toast("AFK Notification", "Now on AFK", "app.ico", 12, True)

# Run
main()