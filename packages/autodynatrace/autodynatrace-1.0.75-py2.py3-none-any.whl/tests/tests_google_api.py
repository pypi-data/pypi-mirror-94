import autodynatrace
import time

from google.cloud import monitoring_v3
from google.oauth2 import service_account


@autodynatrace.trace
def query():
    creds = service_account.Credentials.from_service_account_info(
        {
            "type": "service_account",
            "project_id": "long-ceiling-251107",
            "private_key_id": "7c30dbba31b32c2fa4a304bfd46019c9a41427af",
            "private_key": """-----BEGIN PRIVATE KEY-----
                MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCaIfbuJG2slTPL
                +lhiLrV6Rq/Oo8yOn92XN9ydxfL1Cc8YVSj3PUsLQQCwhk5+SweEycIU5d0OZlKC
                908c/TZJ8vcpFPtnx0ZsOQC3ZbSNiL7ijQ6v006Gnpfa6wiA1rSNNFKTlPMZtabm
                I2GPr03W5orak00BpIq7HFRUfsLrB778DeQCk0g/2wtVjlyYkFIjdwpOG4i4yDML
                NvDO9wVvvpnBwPi8LIG0scRlAKZ5W/Dw7dGnNCrBBwBB8RrvepK8+09z8HJectzr
                qGeYTrFRkxqZ954lfQ26krEiQeouohmXnUXJ95CKLdF2ToiUP8MFWbQAtPUTI1/Z
                k4rhyGXtAgMBAAECggEABPwXN9FuyJeUssKYbCh1jwxNMEIk4fHyoSrZ1DJsLpeQ
                HonWhtRxIl6KTqsxS61Sg21g/PsIIKiXf4vO/7GCuXaFnssCbHNJ6EMZrlS4N6GW
                Bs6oDHCph/oGEDrsrfoDodNw3jwBdrHkwWmghJyXSF1xXStJYMW5BN8gLRFibWZo
                YattiRYB+TPz1Yy6UG09in17YMNr2qSQL+ih7yW/fkkh4U+2tzVWfNzHyUEXEHId
                fot04n6zSApHgVQFmyGNQKKaOq92B5Tftvmjrptdq9qXq9cnZCvPVxNbrNB7dqTb
                XUGfxb9RAKOQGCnQs5QlFosjy9YOs96TUZlpgdf2kQKBgQDJ533LHzcXUB540ZQz
                9fqFdOZAwvgOBryUxN1NyFDMul5MygCocKqlqhBqOW7QEYgqHSuaDE79FAp02d6d
                ua8GMCk93PrE3jv5128N+3sJTjgHqUqETTqhl2MyHOtGBucJQBTxZmmP0HlQmscg
                Yb9dv5HmbfpN1LIoaDDogT/XdQKBgQDDbdg9i03Pj0zX57yTY4echZ4Hak9PNK6y
                NRmUjv3VLdedS5+y7IE7YCw8JsDYF5sEC4GL23GONn2oBOfrxMiLI3Rq7zqt6x6D
                b9sPTRqkqj8Mm2yil60xgtJnBkkj7bdRjRnuKVOS8FoCMGPaSjGQfX6RPq6CiN8b
                R4GKu6r9mQKBgQCKR76S4DUmBVxpWPiMwdorjw2nqyCi0qBTr6T2Acy8+qNdKjhb
                JJbrUVdeuSkY3fkJBuN25RkwIYqrzw+1rJefwFpuoSsqrB4dlhvcUrFIhUbAkISV
                qiMOyxVIHCBS3KVdY4M0dfS0Z46+0tKwbeHXvj2ZuRbmOVcvb3SXuPXVhQKBgG0r
                dXqb0PG7uU960qr7FIxpT+gQiRFT+qruYsXMQxvNKf9ieWm4GFEU3mETvPJ57UyL
                KOj5wyuQYQ11ACGCogyn16bM0NjK2RbPa23WwqVtvR7LzBnf5Q4daG/I4R7C8n8J
                9YxHZbpVrdI/Oeh9Pcbbc9KrU0z0LL3Oah0XzOMxAoGAQPrqmj2oCVeotNX9QYIT
                Vc/y5HjXof/refBYYPyMsxY74UBsEoLHUJC0ifiMs0ostNSWlctPaCj33Q80xYGl
                pMEY5z7pDKMOojJlMJfwj+HF1vtjwQKj5733sLJhdz9jYvcLPQ4ziYBUr0eqPkJx
                rfT4h435Os9jlaBaMx+iLn0=
                -----END PRIVATE KEY-----
                """,
            "client_email": "dynatrace-monitoring@long-ceiling-251107.iam.gserviceaccount.com",
            "client_id": "114422193978788201994",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dynatrace-monitoring%40long-ceiling-251107.iam.gserviceaccount.com",
        }
    )
    client = monitoring_v3.MetricServiceClient(credentials=creds)
    interval = monitoring_v3.types.TimeInterval()
    now = time.time()
    # the data can be up to 4 minutes late
    interval.end_time.seconds = int(now - 240)
    interval.start_time.seconds = int(now - 30000)

    results = client.list_time_series(
        "projects/long-ceiling-251107",
        f'metric.type = "pubsub.googleapis.com/topic/send_request_count"',
        interval,
        monitoring_v3.enums.ListTimeSeriesRequest.TimeSeriesView.FULL,
        timeout=5.0,
    )
    print(len(list(results)))


def main():
    while True:
        query()
        time.sleep(60)


if __name__ == "__main__":
    main()
