import redis
import autodynatrace
import time


@autodynatrace.trace
def main():
    r = redis.Redis(host="192.168.15.101")
    r.mset({"Croatia": "Zagreb", "Bahamas": "Nassau"})
    print(r.get("Bahamas"))
    time.sleep(10)


if __name__ == "__main__":
    main()


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
st = logging.StreamHandler()
fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(thread)d - %(filename)s:%(lineno)d - %(message)s")
st.setFormatter(fmt)
log.addHandler(st)
