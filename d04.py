from shared_use import read_file

def main():
    raw_data = read_file('d04')
    print(raw_data)

    red_elf = 0
    red_elf_2 = 0
    for elves in raw_data:
        elf_a, elf_b = elves.split(',')
        elf_a_min, elf_a_max = elf_a.split('-')
        elf_b_min, elf_b_max = elf_b.split('-')
        elf_a_min, elf_a_max = int(elf_a_min), int(elf_a_max)
        elf_b_min, elf_b_max = int(elf_b_min), int(elf_b_max)

        if elf_a_min <= elf_b_min <= elf_b_max <= elf_a_max:
            red_elf += 1
        elif elf_b_min <= elf_a_min <= elf_a_max <= elf_b_max:
            red_elf += 1

        if elf_a_min <= elf_b_min <= elf_a_max or elf_a_min <= elf_b_max <=elf_a_max:
            red_elf_2 += 1
        elif elf_b_min <= elf_a_min <= elf_b_max or elf_b_min <= elf_a_max <=elf_b_max:
            red_elf_2 += 1


    print(red_elf, red_elf_2)



    return

if __name__ == '__main__':
    print('Running day 04')
    main()
