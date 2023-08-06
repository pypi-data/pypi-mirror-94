"Play with Heads or Tails and receive if you won or not."

if __name__ == '__main__':
    raise Exception(f"Unable to load application file as __main__ level")

def run():
    from aleat3 import Aleatoryous

    coin = Aleatoryous()
    side = coin.single()

    if coinToBinary(side) == 1:
        print("You voted for Head")
    else:
        print("You voted for Tails")

    if coinToBinary(coin.single()) == coinToBinary(side):
        print("You win!!!")
    else:
        print("You lose!!!")
    e = input("Done")
