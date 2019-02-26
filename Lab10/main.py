import csv
import time

def readUsers(fileName):
    users = {} #user: all songs
    songs ={} #song: all users
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

            if songId in songs:
                songs[songId].add(user)
            else:
                songs[songId] = {user}


    return users, songs

def main():
    start = time.time()
    users, songs = readUsers('facts-nns.csv')
    f = open('results99.txt', 'w+')

    startA = time.time()
    count = 1;
    for u in users.keys(): #u: user
        if count > 100:
            break
        count = count+1

        jaccard = set()
        checked = set()
        for s in users[u]: #users: użytkownik: wszystkie piosenki
            for ux in songs[s]: #songs = piosenka: wszyscy uzytkownicy
                if ux not in checked:
                    checked.add(ux)
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
                        jaccard.add(tuple([ux, j]))

        jaccard2 = sorted(jaccard, key=lambda record: record[1], reverse=True)

        f.write(f'User = {u}\n')
        for ii in jaccard2[0:100]:
            f.write('{:9d} {:7.5f}\n'.format(ii[0], ii[1]))

    f.close()
    print('Execusion time: ', time.time() - start)
    print('Algorithm time: ', time.time() - startA)

if __name__ == '__main__':
    main()