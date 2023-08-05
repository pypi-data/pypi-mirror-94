from suds.client import Client


def main():
    c = Client("http://consulta.confirmeonline.com.br/Integracao/Consulta?wsdl")
    print(c)


if __name__ == "__main__":
    main()
