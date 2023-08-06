import arweave
import requests
import os
import sys
import qrcode
from bs4 import BeautifulSoup as BS
import pandas as pd
import json
import matplotlib.pyplot as plt


KEYFILE_PATH = '/path/to/keyfile.json'


def connect(jwk):
    wallet = arweave.Wallet(jwk)
    return wallet


class Fqrweave(object):
    def __init__(self, jwk):
        """

        using https://github.com/MikeHibbert/arweave-python-client
        to connect to Arweave blockchain

        :param: jwk
        """
        self.jwk = jwk
        self.wallet = connect(self.jwk)

    def login(self):
        """
        assign jwk path passed to FQR_WEAVE()
        to connect() function for an easier
        connection with Arweave
        :return: jwk.json path
        """
        global KEYFILE_PATH
        KEYFILE_PATH = self.jwk

        return KEYFILE_PATH


class Tools(object):
    def __init__(self):
        self.wallet = connect(KEYFILE_PATH)

    def pub_address(self):
        return self.wallet.address

    def balance(self):
        """
        :return: wallet's balance in AR or winston * 1E18
        """
        return self.wallet.balance

    def get_max_uploads(self):
        """
        use arweave HTTP api to retrieve 1 byte price in winston
        self.wallet.balance * 1e18 : transform wallet's balance back to winston

        :return: max approx uploads size to the blockweave in mb
        """
        re = requests.get('https://arweave.net/price/1')
        b_price = int(re.text)
        return self.wallet.balance * 1e18 / b_price / 1e6

    def get_n_generators(self):
        """
        use arweave HTTP API to get fQR Weave
        wallet's latest tx

        -----------------------------------------
        fqrweave_addr is owned by fQR Weave team
        and used to send data tx in a form of list

        length: 1

        element: string of jwk['n'] of verified generators
        seperated by a whitespace

        nb of verified generators =
        len((str(last_tx.data, 'utf8')).split(' ')) - 1
        -----------------------------------------

        :return: list of jwk['n'] verified addresses
        """
        fqrweave_addr = 'MtgIRVxVRaooHlL3vHE4Bu875vtnDelgJzwrZ7WnDyo'
        url = f'https://arweave.net/wallet/{fqrweave_addr}/last_tx'
        re = requests.get(url)  # Sends HTTP GET Request
        last_tx = arweave.Transaction(self.wallet, id=re.text)
        last_tx.get_transaction()
        last_tx.get_data()

        #decode from bytestr to ascii, then split it
        #into a list
        return (str(last_tx.data, 'utf8')).split(' ')

    def isverified(self, tx_id):
        """

        :param tx_id:
        :return:
        """
        n_list = Tools().get_n_generators()
        re = requests.get(f'https://arweave.net/tx/{tx_id}/owner').text
        if re in n_list:
            return ('found, gennerated from a verified generator')
        else:
            return ('invalid tx id / not verified')

    def usd_to_ar(self, usd):
        api = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=arweave&vs_currencies=usd')
        json_res = api.json()
        price = json_res["arweave"]["usd"]
        return usd / price


class Generator(object):
    def __init__(self):
        self.wallet = connect(KEYFILE_PATH)

    def batch_generator(self, instance, data_list, dir_name):
        """
        this function scrap generator's instance to extract
        <label>.value text , which represent fQR metadata.

        Then the second parameter contains an array of
        value to be passed to each label.

        After that a data tx is submitted to the blockweave
        with a pre_defined HTML template: _html_1 & _html_2
        and a tag('Content Type', 'text/html') to make the browser
        read the data as html

        transaction.id is encoded to a QR code and saved as .png
        file in dir_name

        :param instance: custom generator instance url
        :param data_list: labels entries
        :param dir_name: path to directory to save the QRs.png
        :return:QR.png transaction's ID
        """
        self.instance = instance
        self.data_list = data_list

        path = os.path.join(sys.path[0], dir_name)

        _html_1 = '<html>' + '<head></head>' + \
                  '<body> <center><h1>verified fQR</h1> </center>' + \
                  '< br > < br > < center > < div > < table > < tr > < th > Data < / th > < th > info < / th > < / tr >'

        _html_2 = '</table></div></body></html>'


        if self.instance.startswith('https://'):
            url = self.instance
        else:
            url = f"https://arweave.net/{self.instance}"

        re = requests.get(url)
        html = BS(re.text, features="lxml")
        labels = html.find_all('label')

        product_metadata = []  # store all generator instance metadata
        table_data = []
        html_table = []

        for element in labels:
            clean_1 = str(element).replace('<label for="product">', '')
            clean_2 = str(clean_1).replace('</label>', '')
            clean_3 = clean_2.split(':')
            clean_4 = clean_3[0]
            product_metadata.append(clean_4)

        if len(self.data_list) != len(product_metadata):
            return 'unmatched arguments'
        else:
            for entry in range(len(self.data_list)):
                entry_data = [product_metadata[entry - 1], self.data_list[entry - 1]]
                table_data.append(entry_data)


        for tb in table_data:
            table_el = f'<tr><td>{tb[0]}</td><td>{tb[1]}</td></tr>'
            html_table.append(table_el)

        fqr_html = _html_1 + ''.join(html_table) + _html_2
        modified_html = (fqr_html.replace(' ', ''))

        transaction = arweave.Transaction(self.wallet, data=modified_html)
        transaction.add_tag('Content-Type', 'text/html')
        transaction.add_tag("App-Name", "fQR-Weave")
        transaction.add_tag("Version", "0.1.5")
        transaction.add_tag("Type", "static")
        transaction.sign()
        transaction.send()

        transaction_fee = arweave.Transaction(self.wallet, quantity=Tools().usd_to_ar(0.005),
                                              to='BbODAb919DcZjX-50a2dzR1EvLK8zbGpr47bQikGCm4' )
        transaction_fee.add_tag("App-Name", "fQR-Weave")
        transaction_fee.add_tag("Version", "0.1.5")
        transaction_fee.add_tag("Type","fee")
        #amount in AR, not winston
        transaction_fee.add_tag("Value", str(Tools().usd_to_ar(0.005)) )
        transaction_fee.sign()
        transaction_fee.send()


        qr = qrcode.QRCode(
            version=3,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(transaction.id)
        qr.make(fit=True)

        img = qr.make_image(fill_color="purple", back_color="white")
        img.save(f'{path}\\{transaction.id}.png')

        return transaction.id

    def csv_generator(self, file_path, instance, dir_path):  # path, generator instance
        """

        :param file_path:
        :param instance:
        :return:
        """
        # connect to generator instance
        if instance.startswith('https://'):
            url = instance
        else:
            url = f"https://arweave.net/{instance}"

        ##############################################

        # get generator entries
        re = requests.get(url)
        html = BS(re.text, features="lxml")
        labels = html.find_all('label')

        product_metadata = []  # store all generator instance metadata

        _html_1 = '<html>' + '<head></head>' + \
                  '<body> <center><h1>verified fQR</h1> </center>' + \
                  '< br > < br > < center > < div > < table > < tr > < th > Data < / th > < th > info < / th > < / tr >'

        _html_2 = '</table></div></body></html>'

        for element in labels:
            clean_1 = str(element).replace('<label for="product">', '')
            clean_2 = str(clean_1).replace('</label>', '')
            clean_3 = clean_2.split(':')
            clean_4 = clean_3[0]
            product_metadata.append(clean_4)

        ################################################

        df = pd.read_csv(file_path)
        header = list(df.head(0).columns)
        if header != product_metadata:
            return 'unmatched entries'

        rows = []

        # add each a row as a list `rows` list
        for i, j in df.iterrows():
            rows.append(list(j))

        # create array (_html_body) of arrays (metadata: data ; html table elements)
        _html_body = []
        for product in rows:
            components = []  # stores each product's html table element in a array and append it to _html_body
            for i in range(len(header)):
                div = f'<tr><td>{header[i]}</td><td>{product[i]}</td></tr>'
                components.append(div)
            _html_body.append(components)

        for html_el in _html_body:
            fqr_html = _html_1 + ''.join(html_el) + _html_2
            fqr = fqr_html.replace(' ', '')

            transaction = arweave.Transaction(self.wallet, data=fqr)
            transaction.add_tag('Content-Type', 'text/html')
            transaction.add_tag("App-Name", "fQR-Weave")
            transaction.add_tag("Version", "0.1.5")
            transaction.add_tag("Type", "static")
            transaction.sign()
            transaction.send()

            transaction_fee = arweave.Transaction(self.wallet, quantity=Tools().usd_to_ar(0.005),
                                                  to='BbODAb919DcZjX-50a2dzR1EvLK8zbGpr47bQikGCm4')
            transaction_fee.add_tag("App-Name", "fQR-Weave")
            transaction_fee.add_tag("Version", "0.1.5")
            transaction_fee.add_tag("Type", "fee")
            transaction_fee.add_tag("Value", str(Tools().usd_to_ar(0.005)))
            transaction_fee.sign()
            transaction_fee.send()

            qr = qrcode.QRCode(
                version=3,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(transaction.id)
            qr.make(fit=True)
            path = os.path.join(sys.path[0], dir_path)
            img = qr.make_image(fill_color="purple", back_color="white")
            img.save(f'{path}\\{transaction.id}.png')

        return None


class DynamicStats(object):  # __version__== 0.0.5

    def __init__(self, api_key):
        """
        OPTION 1:
        Using cutt.ly as third party
        shortner and analytics provider


        :param api_key: cutt.ly api key
        """
        self.api_key = api_key
        self.wallet = connect(KEYFILE_PATH)

    def generate_dfqr(self, instance, metadata, dir):

        fqr_1 = Generator().batch_generator(instance=instance, data_list=metadata, dir_name=dir)

        short_url = f"https://cutt.ly/api/api.php?key={self.api_key}&short=https://arweave.net/{fqr_1}&name={fqr_1}"
        data = requests.get(short_url).json()["url"]


        fqr2_html = '<html><head></head>' + \
                    '<body><center><h1>Dynamic fQR</h1></center><br><br><center>' + \
                    f'<center><br><br><br><script>window.location.replace("{data["shortLink"]}")</script></center></body></html>'

        html = ''.join(fqr2_html)

        # post tx_2
        tx = arweave.Transaction(self.wallet, data=html)
        tx.add_tag('Content-Type', 'text/html')
        tx.sign()
        tx.send()

        # generate QR code for tx_2 (redirection page)
        qr = qrcode.QRCode(
            version=3,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(tx.id)
        qr.make(fit=True)

        img = qr.make_image(fill_color="purple", back_color="white")
        img.save(f'{dir}\\DFQR@{tx.id}.png')

        return tx.id

    def scans_count(self, tx_id):
        """


        :param tx_id: tx2 ID
        :return: clicks count
        """
        r = requests.get(
            f'https://cutt.ly/api/api.php?key={self.api_key}&stats=https://cutt.ly/{tx_id}')
        clicks = json.loads(r.text)["stats"]["clicks"]
        return int(clicks)

    def get_date(self, tx_id):
        """

        :param tx_id:
        :return:
        """

        r = requests.get(
            f'https://cutt.ly/api/api.php?key={self.api_key}&stats=https://cutt.ly/{tx_id}')
        date = json.loads(r.text)["stats"]["date"]
        return date

    def get_browsers(self, tx_id):
        """

        :param tx_id:
        :return:
        """

        r = requests.get(
            f'https://cutt.ly/api/api.php?key={self.api_key}&stats=https://cutt.ly/{tx_id}')
        browsers = json.loads(r.text)["stats"]["devices"]["bro"]
        kv_list = []

        labels = list(browsers['0'].keys())
        kv_list.append(labels)

        for browser in browsers:
            v = (list(browsers[browser].values()))
            kv_list.append(v)
        return kv_list

    def plot_browsers(self, tx_id):
        """

        :param tx_id:
        :return:
        """
        data = DynamicStats(self.api_key).get_browsers(tx_id)
        labels = data.pop(0)
        browsers = []
        clicks = []
        for browser in data:
            browsers.append(browser[0])
            clicks.append(int(browser[1]))

        plt.bar(browsers, clicks, color='purple', width=0.5)
        plt.title("Browsers Used In The Scan")
        plt.xlabel("Browsers")
        plt.ylabel("Scans")
        plt.show()

        return None

    def get_countries(self, tx_id):
        """

        :param tx_id:
        :return:
        """

        r = requests.get(
            f'https://cutt.ly/api/api.php?key={self.api_key}&stats=https://cutt.ly/{tx_id}')
        browsers = json.loads(r.text)["stats"]["devices"]["geo"]
        print(json.loads(r.text)["stats"])
        kv_list = []

        labels = list(browsers['0'].keys())
        kv_list.append(labels)

        for browser in browsers:
            v = (list(browsers[browser].values()))
            kv_list.append(v)
        return kv_list

    def plot_countries(self, tx_id):
        """

        :param tx_id:
        :return:
        """
        data = DynamicStats(self.api_key).get_countries(tx_id)
        labels = data.pop(0)
        countries = []
        clicks = []
        for country in data:
            countries.append(country[0])
            clicks.append(int(country[1]))

        plt.bar(countries, clicks, color='purple', width=0.5)
        plt.title('scan per country')
        plt.xlabel('country')
        plt.ylabel('scans')
        plt.show()

        return None

    def get_devices(self, tx_id):
        """

        :param tx_id:
        :return:
        """

        r = requests.get(
            f'https://cutt.ly/api/api.php?key={self.api_key}&stats=https://cutt.ly/{tx_id}')
        devices = json.loads(r.text)["stats"]["devices"]["dev"]
        print(json.loads(r.text)["stats"])
        kv_list = []

        labels = list(devices['0'].keys())
        kv_list.append(labels)

        for device in devices:
            v = (list(devices[device].values()))
            kv_list.append(v)
        return kv_list




