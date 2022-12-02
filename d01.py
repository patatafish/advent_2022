from shared_use import read_file


def count_inventory(my_data):
    inventory = []
    elf_has = 0

    for line in my_data:
        if line:
            elf_has += int(line)
        else:
            inventory.append(elf_has)
            elf_has = 0

    inventory.sort()
    inventory.reverse()
    return inventory


def main():
    raw_data = read_file('d01', 'l')

    print(raw_data)

    elf_food = count_inventory(raw_data)
    print(elf_food[0], elf_food[1], elf_food[2])
    print(elf_food[0] + elf_food[1] + elf_food[2])


if __name__ == '__main__':
    print('Running day 1 directly')

    main()
