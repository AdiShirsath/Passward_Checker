import requests
import hashlib


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    print(url)
    if res.status_code != 200:
        raise RuntimeError(f'error fetching {res.status_code},check api and try again')
    return res


def get_password_leak_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pawned_api_check(password):
    sha1password = (hashlib.sha1(password.encode('utf-8')).hexdigest().upper())
    first5 = sha1password[:5]
    tail = sha1password[5:]

    response = request_api_data(first5)
    return get_password_leak_count(response, tail)


def main(args):
    for password in args:
        count = pawned_api_check(password)
        if count:
            print(f'{password} was found {count} times!!!! ')
            print('you should change yours password')
        else:
            print(f"{password} was not found you don't need to change it")
    return 'done!'


if __name__ == "__main__":
   password = open('password.txt')

   main(password)
