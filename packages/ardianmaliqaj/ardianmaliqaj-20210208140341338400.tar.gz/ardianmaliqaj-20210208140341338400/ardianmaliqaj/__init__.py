class read_csv:
    def __init__(this, name):
        this.name = name
        this.file = open(this.name, 'r').readlines()
        this.len = len(this.file)
        this.header = [this.file[0]]
        this.body = this.file[1:]

    def __str_(this):
        return str(list(this.file))

    def __iter__(this):
        return iter(this.file)

    def __getitem__(this, index):
        return this.file[index]

    def split(this, limit = 1000):
        for n, x in enumerate(this.body):
            if n % limit == 0:
                header, body = this.header, this.body[n: n + limit]
                open("{}_{}.csv".format(n, this.name), 'w+').writelines(header + body)


