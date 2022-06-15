import os
import sys
import cloudscraper
from bs4 import BeautifulSoup
from twocaptcha import TwoCaptcha


def resolve_recaptcha(my_api_key):
    try:
        solver = TwoCaptcha(my_api_key)
        result = solver.recaptcha(url='https://sistema.ac/login', sitekey="6Lfnc3MaAAAAABhkKfSCEZFtCbHnpkVvvExpbVjB")
        return result['code']
    except Exception as exc:
        print('Error in resolve', exc)
        return False


def read_lines(path):
    if os.path.isfile(path):
        return [line.rstrip() for line in open(path)]
    return False


def append_to_file(path, newline):
    try:
        fp = open(path, "a+")
        fp.write("%s\n" % newline)
        fp.close()
    except Exception as exc:
        print(e)


email = input('EMAIL: ')
password = input('SENHA: ')
chv_cpth = 'fb15d4659c51e0c3e88e10e19dd10530'

print('RECEBENDO DADOS DO SITE')


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'referer': 'https://sistema.ac/login'
}

scrap = cloudscraper.create_scraper()

r1 = scrap.get('https://sistema.ac/login')
print('INICIANDO LOGIN...')
soup = BeautifulSoup(r1.text, 'lxml')
tk = soup.find('input', {'name': '_token'})['value']
pay = {
    '_token': tk,
    'email': email,
    'password': password,
    'g-recaptcha-response': resolve_recaptcha(chv_cpth)
}

r2 = scrap.post('https://sistema.ac/login', data=pay)

r3 = scrap.get(url='https://sistema.ac/bases')

if r3:
    print('LOGIN REALIZADO COM SUCESSO!', email)
else:
    sys.exit()

r4 = scrap.get('https://sistema.ac/bases/12')
soup2 = BeautifulSoup(r4.text, 'lxml')
tk2 = soup2.find('input', {'name': '_token'})['value']
arq = input('Digite o arquivo que será consultado: ')

cpfs = read_lines(arq)
for cpf in cpfs:
    scrap.headers.update({
        'origin': 'https://sistema.ac',
        'referer': 'https://sistema.ac/bases/12',
        'sec-ch-ua': 'Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'x-requested-with': 'XMLHttpRequest'
        })
    pay2 = {
        '_token': tk2,
        'module': 'cpf',
        'doc': cpf[:11],
        'g-recaptcha-response': resolve_recaptcha(chv_cpth)
    }
    r5 = scrap.post('https://sistema.ac/bases/12', params=pay2, data=pay2)
    dadosbico = BeautifulSoup(r5.text, 'html.parser')
#    if = r5.text
    e = dadosbico.find('th', text='SEXO').find_next('td').text
    q = dadosbico.find('th', text='NOME').find_next('td').text
    w = dadosbico.find('th', text='CPF').find_next('td').text
    r = dadosbico.find('th', text='MAE').find_next('td').text
    t = dadosbico.find('th', text='PAI').find_next('td').text
    y = dadosbico.find('th', text='NASC').find_next('td').text
    u = dadosbico.find('th', text='LOCAL NASCIMENTO').find_next('td').text

    a = dadosbico.find('th', text='NUMERO DOCUMENTO').find_next_sibling('td').text
    s = dadosbico.find('th', text='ORGAO EMISSOR').find_next_sibling('td').text

    z = dadosbico.find('th', text='CATEGORIA ATUAL').find_next('td').text
    x = dadosbico.find('th', text='RENACH').find_next('td').text
    c = dadosbico.find('th', text='REGISTRO').find_next('td').text
    v = dadosbico.find('th', text='NUMERO CNH').find_next('td').text
    b = dadosbico.find('th', text='DATA EMISSAO').find_next('td').text
    n = dadosbico.find('th', text='DATA VALIDADE CNH').find_next('td').text
    m = dadosbico.find('th', text='PRIMEIRA CNH').find_next('td').text
    i = dadosbico.find('th', text='UF PRIMEIRA CNH').find_next('td').text

    endereco = dadosbico.find('th', text='ENDERECO').find_next('td').text
    bairro = dadosbico.find('th', text='BAIRRO').find_next('td').text
    cep = dadosbico.find('th', text='CEP').find_next('td').text
    municipio = dadosbico.find('th', text='MUNICIPIO').find_next('td').text
    uf = dadosbico.find('th', text='UF').find_next('td').text

    end = str(f"{cep} {endereco}\n{bairro} - {municipio[8:]}")

    append_to_file((cpf + '.txt'), f"NOME: {q}\nCPF: {w}\nMAE: {r}\nPAI: {t}\nNASC: {y}\nLOCAL: {u[8:]}\nRG\nNUMERO: {a}\nORGAO EMISSOR: {s}\nCNH\nCATEGORIA: {z}\nRENACH: {x}\nREGISTRO: {c}\nESPELHO: {v}\nEMISSAO: {b}\nVALIDADE: {n}\nPRIMEIRA: {m}\n\n{end}")
    print(f"ARQUIVO CRIADO COM SUCESSO!     {cpf}      #2Fe(OH)²")
