from shared_use import read_file


def tsa(my_bags):
    bag_list = []

    for bag in my_bags:
        bag_size = len(bag)/2
        front = bag[int(len(bag)/2):]
        back = bag[:int(len(bag)/2)]

        flag = False
        for item in front:
            if item in back:
                bag_list.append([front, back, item])
                print(bag_list)
                flag = True
            if flag: break


    return bag_list


def tsa2(my_bags):
    security_groups = []
    for i in range(0, len(my_bags)-1, 3):
        j = i+1
        k = i+2
        for item in my_bags[i]:
            flag = False
            if item in my_bags[j] and item in my_bags[k]:
                print([my_bags[i], my_bags[j], my_bags[k], item])
                security_groups.append([my_bags[i], my_bags[j], my_bags[k], item])
                flag = True
            if flag:
                break

    return security_groups


def score_bags(my_bags):
    total = 0

    for bag in my_bags:
        print(bag)
        score = ord(bag[-1])
        if score >= 97:
            score -= 96
        else:
            score -= 38

        print(score)
        total += score

    print(f'Total score:{total}')


def main():
    raw_data = read_file('d03', 'l')
    print(raw_data)

    checked_bags = tsa(raw_data)
    score_bags(checked_bags)
    checked_groups = tsa2(raw_data)
    score_bags(checked_groups)

if __name__ == '__main__':
    print('Running day 3 directly')
    main()
