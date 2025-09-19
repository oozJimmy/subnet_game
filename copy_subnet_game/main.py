from rich import print
from random import randint
from time import time
from typing import Callable, Tuple
from playsound import playsound


def main():
    points = 0
    print("Would you like to play the subnet game?")
    while(True):

        ip_addr = getRandomIP()
        mask = getRandomMask()
        print("Please enter info for this IPv4 address:", formatAddr(ip_addr))
        print("With this subnet mask", formatAddr(mask))

        #ask questions
        (correct, timeTaken) = questionStopwatch(promptSubnetId, ip_addr, mask)
        points += calculatePoints(correct, timeTaken)

        (correct, timeTaken) = questionStopwatch(promptBroadcastAddr, ip_addr, mask)
        points += calculatePoints(correct, timeTaken)

        (correct, timeTaken) = questionStopwatch(promptFirstHostAddr, ip_addr, mask)
        points += calculatePoints(correct, timeTaken)

        (correct, timeTaken) = questionStopwatch(promptLastHostAddr, ip_addr, mask)
        points += calculatePoints(correct, timeTaken)

        #prompt for another address and question set
        user_resp = input("Another round? ")
        if user_resp != 1 and user_resp.lower() != "y":
            break
    print(f"Game over\nYou earned {points} points")

def getRandomIP() -> int:
    return randint(0, 2 ** 32)

def getRandomMask() -> int:
    cidr_num = randint(1, 31)
    return ((1 << cidr_num) - 1) << (32 - cidr_num)

def getSubnetId(addr:int, subnet_mask:int) -> int:
    return addr & subnet_mask

def getBroadcastAddr(addr:int, subnet_mask:int) -> int:
    subnet_id = getSubnetId(addr, subnet_mask)
    wildcard_mask = 0xFFFFFFFF ^ subnet_mask
    return subnet_id | wildcard_mask

def getFirstHostAddr(addr:int, mask:int) -> int:
    return getSubnetId(addr, mask) + 1

def getLastHostAddr(addr:int, mask:int) -> int:
    return getBroadcastAddr(addr,mask) - 1

def formatAddr(addr: int) -> str:
    octets:list[int] = []
    for i in range(3, -1, -1):
        octets.append((addr >> (i * 8)) & 0xFF)
    return ".".join(list(map(str, octets)))

def ip_addr_stoi(addr:str) -> int:
    octets = list(map(int, addr.split(".")))
    dec_octets = []

    for i in range(4):
        dec_octets.append(octets[i] << ((3 - i) * 8))

    return sum(dec_octets)

def checkAnswer(answer:int, derived_ans:int) -> bool:
    if answer != derived_ans:
        print(f"[red]Incorrect! The correct answer was {formatAddr(derived_ans)}")
        playsound("sounds/incorrect_sound.mp3", block=False)
        return False
    print("[green]Correct!")
    playsound("sounds/correct_sound.mp3", block=False)
    return True

def questionStopwatch(arg_func:Callable[[int, int], int], addr:int, mask: int) -> Tuple[bool, float]:
    startTime = time()
    correct = bool(arg_func(addr, mask))
    return (correct, time() - startTime)

def promptSubnetId(addr:int, mask:int) -> int:
    subnet_id = input("Enter the subnet id: ")
    return checkAnswer(ip_addr_stoi(subnet_id), getSubnetId(addr, mask))

def promptBroadcastAddr(addr:int, mask:int) -> int:
    broadcast_addr = input("Enter the broadcast address: ")
    return checkAnswer(ip_addr_stoi(broadcast_addr), getBroadcastAddr(addr, mask))

def promptFirstHostAddr(addr:int, mask:int) -> int:
    first_host_addr = input("Enter the first host address: ")
    return checkAnswer(ip_addr_stoi(first_host_addr), getFirstHostAddr(addr, mask))

def promptLastHostAddr(addr:int, mask:int) -> int:
    last_host_addr =  input("Enter the last host address: ")
    return checkAnswer(ip_addr_stoi(last_host_addr), getLastHostAddr(addr, mask))

def calculatePoints(correct: bool, timeTaken: float) -> int:
    return (int(correct) * 25) + max(0, round(50 - 10 * (timeTaken - 2)))

if __name__ == "__main__":
    main()
