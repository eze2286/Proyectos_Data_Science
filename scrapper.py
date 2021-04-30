import requests
import lxml.html as html
import os
import datetime
encabezados  = {
    "user-agent" : "Mozilla / 5.0 (X11; Linux x86_64) AppleWebKit / 537.36 (KHTML, como Gecko) Ubuntu Chromium / 71.0.3578.80 Chrome / 71.0.3578.80 Safari / 537.36" ,
}
home_url = 'https://www.ambito.com/'
Links = '//div[@class="info-wrapper"]/h2/a/@href'
Titulos = '//h1[@class="title"]//text()'
Resumen = '//h2[@class="excerpt"]//text()'
Cuerpo = '//section[@class="body-content note-body content-protected-false"]//text()'

def parse_notice(link, today):
    try:
        response = requests.get(link, encabezados)
        if response.status_code == 200:
            #notice = response.text
            notice=response.content
            parsed = html.fromstring(notice)
            try:
               title = parsed.xpath(Titulos)[0].strip()
               title = title.replace('\"', '').replace("?", "").replace("¿", "").replace(":", " ").replace("/", "-")
               summary = parsed.xpath(Resumen)[0].strip()
               body_base = parsed.xpath(Cuerpo)[0:]
               body_final = ""
               for linea in body_base:
                    body_final += " " + linea.replace("\n", "").strip()
                        #print(linea)
    

            except IndexError:
                return
            with open(f'{today}/{title}.txt', "w", encoding = "utf-8") as f:
                f.write(title)
                f.write("\n\n")
                f.write(summary)
                f.write("\n\n")
                f.write(body_final)
                f.write("\n")
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)




def parse_home():
    try:
        response = requests.get(home_url, encabezados)
        ##links_cronista_completo = []
        if response.status_code == 200:
            #home = response.text 
            home=response.content
            parse = html.fromstring(home)  # Usando lxml me transforma el codigo html de requests a codigo xpath
            links_xpath = parse.xpath(Links)
            ##for link in links_xpath:
                ##links_cronista_completo.append("https://www.cronista.com"+link)
            #print(links_cronista_completo)

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_xpath:
                parse_notice(link, today)

        else:
            raise ValueError(f"Error {response.status_code}")
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == "__main__":
    run()