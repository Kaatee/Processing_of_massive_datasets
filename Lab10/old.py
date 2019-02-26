import csv
import time

def readUsers(fileName):
    users = {}
    with open(fileName, 'r') as file:
        csvReader = csv.reader(file)
        next(csvReader, None)

        for x in csvReader:
            user = int(x[0])
            songId = int(x[1])
            if user in users:
                users[user].add(songId)
            else:
                users[user] = {songId}
    return users

def main():
    start = time.time()
    users = readUsers('facts-nns.csv')
    f = open('old.txt', 'w+')
    startA = time.time()
    count = 1;
    for u in users.keys():
        if count > 100:
            break
        count = count+1

        jaccard =[]
        for ux in users.keys():
            #if bool(users[ux] and users[u]):
                intersect = 0
                if len(users[ux]) >= len(users[u]):
                    for x in users[u]:
                        if x in users[ux]:
                            intersect = intersect + 1

                else:
                    for x in users[ux]:
                        if x in users[u]:
                            intersect = intersect + 1

                union = len(users[ux]) + len(users[u]) - intersect
                if intersect != 0 and union != 0:
                    j = intersect / union
                    jaccard.append([ux, j])

        jaccard2 = sorted(jaccard, key=lambda record: record[1], reverse=True)

        f.write(f'User = {u}\n')
        for ii in jaccard2[0:100]:
            f.write('{:9d} {:7.5f}\n'.format(ii[0], ii[1]))

    f.close()
    print('Time: ', time.time() - startA)

if __name__ == '__main__':
    main()