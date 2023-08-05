import autodynatrace
from suds.client import Client
import time


@autodynatrace.trace
def go():
    c = Client("http://consulta.confirmeonline.com.br/Integracao/Consulta?wsdl")
    c.service.WsViaVarejo("W3800", "Hh34cMJJ", "HUGOG", "35274055850", "", "")


def main():
    while True:
        go()
        time.sleep(10)

    # WsViaVarejo(xs:string usuario, xs:string senha, xs:string sigla, xs:string cpfcnpj, xs:string nome, xs:string telefone)


if __name__ == "__main__":
    main()
