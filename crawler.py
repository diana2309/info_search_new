import os
import requests
from bs4 import BeautifulSoup

# Список URL для скачивания
urls = [
    'https://inde.io/article/25091-rabochiy-vopros-menedzher-po-prodazham-v-inde-administrator-fotograf-v-spartak-space-barmen-v-porto-ronco',
    'https://inde.io/article/6512-na-chto-zhivut-kazantsy-chast-pervaya-programmist-uchastkovyy-terapevt-instabloger-barista-i-prepodavatel-istorii',
    'https://inde.io/article/900-idei-dlya-goroda-dlya-chego-vystavochnym-tsentram-nuzhen-firmennyy-stil',
    'https://inde.io/article/27106-zhit-s-sosedyami-vse-ravno-chto-s-dalnimi-rodstvennikami-kak-seychas-zhivut-studenty-v-s-emnyh-kvartirah',
    'https://inde.io/article/491-slepoe-kino',
    'https://inde.io/article/15588-kult-elvina-greya-muhomor-po-imeni-elvin-fanfiki-nadpisi-iz-mayoneza-i-drugie-proyavleniya-fanatskoy-lyubvi',
    'https://inde.io/article/6060-zaveduyuschaya-galereey-sovremennogo-iskusstva-gmii-rt-to-chto-delaet-smena-kruto-no-odna-institutsiya-fizicheski-ne-mozhet-nasytit-ves-gorod',
    'https://inde.io/article/19402-gid-chto-nado-znat-o-kazanskom-marafone-2019',
    'https://inde.io/article/3045-11-storon-shaymieva-chto-my-uznali-iz-novoy-biografii-pervogo-prezidenta-tatarstana',
    'https://inde.io/article/4687-kakimi-mogut-stat-ulitsa-baumana-ploschad-svobody-i-drugie-obschestvennye-prostranstva-tatarstana',
    'https://inde.io/article/2541-oni-umnye-oni-luchshe-nas-kto-delaet-media-dlya-podrostkov-fraktsiya-i-pochemu-vzroslym-tozhe-polezno-ego-chitat',
    'https://inde.io/article/394-ne-kak-tarantino-3-volnyh-vesterna',
    'https://inde.io/article/12253-kapsuly-s-televizorami-dvuhetazhnyy-loft-i-dom-gde-pushkin-vstretil-baratynskogo-gid-po-kazanskim-hostelam-obnovleno',
    'https://inde.io/article/1674-gid-gde-pod-otkrytym-nebom-tantsuyut-densholl-salsu-i-tango',
    'https://inde.io/article/2042-72-kvadratnyh-metra-v-kakih-domah-i-kvartirah-budut-zhit-rossiyane-buduschego',
    'https://inde.io/article/6371-nuzhno-perestat-zatykat-ushi-spetsialist-po-zvukovomu-landshaftu-o-tom-kak-zvuchit-ulitsa-baumana',
    'https://inde.io/article/21323-v-almetievske-prohodit-pablik-art-proekt-skazki-o-zolotyh-yablokah-rasskazyvaem-kak-izmenitsya-gorod-v-etom-godu',
    'https://inde.io/article/8350-teoriya-razbityh-okon-rabotaet-kurator-anna-nistratova-o-tom-pochemu-u-pablik-arta-v-almetievske-bolshe-shansov-chem-v-moskve',
    'https://inde.io/article/91384-plany-na-vyhodnye-open-space-market-na-parkovke-tsentra-art-otkrytie-vystavki-vostochnyy-stil-v-smene-i-re-actor-fest',
    'https://inde.io/article/14341-eksperiment-kakovo-eto-nedelyu-rabotat-v-ofise-stoya',

    'https://inde.io/article/60885-bylo-ponyatno-chto-nash-proekt-sozdan-dlya-etogo-mesta-kak-chelnintsy-pridumali-i-proveli-festival-v-svoem-gorode',
    'https://inde.io/article/13011-poetessa-dinara-rasuleva-mne-hochetsya-pokazat-chto-byt-zhenschinoy-ne-stydno',
    'https://inde.io/article/31000-gid-chto-delat-na-festivale-breyk-dansa-i-strit-arta-combonation',
    'https://inde.io/article/20625-kritika-patriarhata-i-izuchenie-potrebiteley-marihuany-kakie-knigi-vypuskayut-molodye-rossiyskie-izdatelstva',
    'https://inde.io/article/61816-gid-po-30-avgusta-kuda-idti-i-chto-smotret-na-dne-goroda-i-respubliki',
    'https://inde.io/article/17300-zimnee-chtenie-roman-o-norilskom-vosstanii-komiks-o-feminizme-i-esche-14-novyh-knig',
    'https://inde.io/article/4723-tyurkskiy-gambit-devyat-spektakley-kotorye-nado-uvidet-na-festivale-nauruz',
    'https://inde.io/article/94011-konturnye-karty-kak-hudozhniki-iz-raznyh-gorodov-issledovali-smeh-chernyy-les-i-vodoemy-v-kazanskoy-rezidentsii-i-chto-iz-etogo-poluchilos',
    'https://inde.io/article/21675-dva-goda-nazad-proshla-pervaya-rossiyskaya-molodezhnaya-arhitekturnaya-biennale-chto-proizoshlo-s-ee-uchastnikami',
    'https://inde.io/article/33551-kakim-budet-novyy-park-manzara-u-kremlevskoy-damby',
    'https://inde.io/article/50435-dvizhenie-navstrechu-pyat-prichin-poyti-na-vystavku-moving-women-v-smene',
    'https://inde.io/article/48749-totalnyy-gid-po-novomu-knizhnomu-festivalyu-smeny',
    'https://inde.io/article/5383-dolce-avito-desyat-strannyh-uslug-dlya-teh-kto-proboval-v-zhizni-vse',
    'https://inde.io/article/1560-muzykant-filipp-gorbachyov-v-vechnost-vhodit-tolko-lyubov',
    'https://inde.io/article/585-50-ottenkov-shutok-pro-chyornyh',
    'https://inde.io/article/73275-plany-na-nedelyu-spetspokaz-filma-korolevstvo-polnoy-luny-v-kinomaks-imax-jazz-blues-v-rockstar-bar-i-kontsert-komikov-v-gole',
    'https://inde.io/article/27848-eto-nenormalno-ubirat-peshehodnye-perehody',
    'https://inde.io/article/26185-koronavirus-kogda-nibud-zakonchitsya-a-dollar-po-80-net-kazanskie-restoratory-rassuzhdayut-o-posledstviyah-pandemii-i-krizisa',
    'https://inde.io/article/18114-innovatsionnyy-kulturnyy-i-gastronomicheskiy-pridumyvaem-molodezhnye-turisticheskie-marshruty-po-kazani',
    'https://inde.io/article/8606-pochti-passivnyy-dohod-vosem-prostyh-no-legalnyh-sposobov-zarabotat-v-kazani',

    'https://inde.io/article/17368-burkini-hidzhaby-i-shtany-sultanki-gde-musulmankam-pokupat-sportivnuyu-odezhdu',
    'https://inde.io/article/289-redaktsiya-slushaet',
    'https://inde.io/article/95242-kupol-tsirka-sotsgorod-i-tramvaynoe-koltso-17-horoshih-ekskursiy-po-kazani-na-kotorye-stoit-shodit-v-yanvare',
    'https://inde.io/article/11022-kariernyy-razvorot-kak-prepodavatelnitsa-turetskogo-stala-yuvelirom-a-konfliktolog-fitnes-trenerom-i-horeografom',
    'https://inde.io/article/11289-vsem-ne-hvataet-professionalov-v-oblasti-iskusstva-gid-po-chastnym-hudozhestvennym-galereyam-kazani-ot-inde-i-diny-ahmetovoy',
    'https://inde.io/article/71910-rabochiy-vopros-arhitektor-v-byuro-cheharda-kontent-meyker-v-pike-guides-i-marketolog-v-deva-monoi',
    'https://inde.io/article/30060-rabochiy-vopros-redaktor-novostey-na-sayt-harper-s-bazaar-barmeny-v-more-i-razrabotchiki-v-ak-bars-tsifrovye-tehnologii',
    'https://inde.io/article/870-redaktsiya-slushaet',
    'https://inde.io/article/407-guilty-pleasure-5-desertov-ot-kotoryh-hochetsya-tolstet',
    'https://inde.io/article/20609-rabochiy-vopros-vospitatel-barmen-administrator-i-grumer',
    'https://inde.io/article/1404-nuzhno-sdelat-eschyo-tri-shtaba-i-odnu-smenu-kazan-kotoroy-net-v-kommentariyah-uchastnikov-madeinkazan',
    'https://inde.io/article/34358-rabochiy-vopros-investor-dlya-chop-chop-sotrudniki-v-cups-i-voditel-parovozika-kremlevskoy-naberezhnoy',
    'https://inde.io/article/16454-ugolok-potrebitelya-besplatnyy-kofe-v-cofix-skidki-v-the-body-shop-i-tovary-k-hellouinu-v-ashane',
    'https://inde.io/article/37530-instruktsiya-kak-zaschititsya-ot-kleschey-v-2021-godu-i-chego-ot-nih-zhdat',
    'https://inde.io/article/25915-rabochiy-vopros-press-sekretar-v-grintu-dizayner-vo-fragency-i-menedzher-po-kommunikatsiyam-v-arhideti',
    'https://inde.io/article/27694-ugolok-potrebitelya-promokody-open-space-market-rasprodazha-v-forever-yang-shope-i-dr-martens-so-skidkoy-na-asos',
    'https://inde.io/article/21283-rabochiy-vopros-koordinator-proektov-v-smenu-malyar-v-qullar-pekar-konditer-na-kazanskiy-hlebozavod-2',
    'https://inde.io/article/6225-reviziya-devyat-kazanskih-sekond-hendov-iz-kotoryh-ne-uyti-s-pustymi-rukami',
    'https://inde.io/article/25521-pyat-idey-dlya-pozdravleniy-audiogid-s-priznaniyami-birthday-burger-i-vzglyad-s-neba',
    'https://inde.io/article/54167-mestnye-14-biznesov-iz-tatarstana-i-stolko-zhe-skidok-dlya-chitateley-inde',

    'https://inde.io/article/1018-gid-chto-smotret-i-gde-vypit-v-noch-muzeev-2016',
    'https://inde.io/article/34089-rabochiy-vopros-kreativnyy-prodyuser-v-vagimagia-shef-povar-v-istinu-i-rukovoditel-fotoshkoly-pikcha-v-kazani',
    'https://inde.io/article/24114-rabochiy-vopros-upakovschik-podarkov-v-l-etual-ofitsiant-v-sol-grous-haker-v-radeant',
    'https://inde.io/article/24220-ugolok-potrebitelya-dnevnaya-skidka-v-paloma-cantina-rasprodazha-v-chitay-gorode-i-minus-20-protsentov-na-asos',
    'https://inde.io/article/2119-krov-ne-budet-zhdat-kto-sdaet-zhilie-v-kazani-na-airbnb',
    'https://inde.io/article/18875-ugolok-potrebitelya-kombo-v-kystybyy-ovsyanoe-moloko-po-skidke-v-eurospar-i-merch-ot-nyx',
    'https://inde.io/article/3699-ugolok-potrebitelya-prilozhenie-dlya-zakaza-kofe-v-nefti-mezhsezonnaya-rasprodazha-v-h-m-i-skidki-dlya-parochek-v-outpac',
    'https://inde.io/article/48329-rabochiy-vopros-storiteller-v-kamu-povar-v-cicheti-i-spetsialist-v-fond-institut-razvitiya-gorodov',
    'https://inde.io/article/34642-11-par-ultramodnoy-obuvi-na-zimu-esli-vam-vse-esche-nechego-nosit',
    'https://inde.io/article/9907-spetsvypusk-ugolka-potrebitelya-luchshie-aktsii-vremennye-i-postoyannye-dlya-kazanskih-studentov',
    'https://inde.io/article/1984-natsii-fastfuda-kak-razvit-vnutrenniy-turizm-s-pomoschyu-makflurri-iz-koniny-i-napolnitelya-iz-ezha-i-uzha',
    'https://inde.io/article/3246-ugolok-potrebitelya-pitstsa-v-forme-serdtsa-v-dodo-aktsiya-na-klubniku-v-perekrestke-i-novye-lanchi-v-hlebe-i-vine',
    'https://inde.io/article/445-redaktsiya-slushaet',
    'https://inde.io/article/25521-pyat-idey-dlya-pozdravleniy-audiogid-s-priznaniyami-birthday-burger-i-vzglyad-s-neba',
    'https://inde.io/article/9873-rabochiy-vopros-press-sekretar-parkov-i-skverov-stsenarist-v-videoprodakshn-proektnyy-piarschik-lektoriya-pro-seks-i-znatok-vina-v-bar',
    'https://inde.io/article/8557-ugolok-potrebitelya-mezhsezonnaya-rasprodazha-v-ekonike-novaya-kollektsiya-v-corner17-i-skidka-na-arendu-dekora-v-home-story',
    'https://inde.io/article/43785-rabochiy-vopros-tovaroved-v-samokat-smm-menedzher-v-teatr-imeni-tinchurina-i-administrator-barista-v-yaratam',
    'https://inde.io/article/11022-kariernyy-razvorot-kak-prepodavatelnitsa-turetskogo-stala-yuvelirom-a-konfliktolog-fitnes-trenerom-i-horeografom',
    'https://inde.io/article/20807-ugolok-potrebitelya-rasprodazha-v-12storeez-besplatnaya-dostavka-ot-filtra-i-spetsialnoe-predlozhenie-v-uniqlo',
    'https://inde.io/article/24056-ugolok-potrebitelya-skidka-na-zavtraki-v-holy-bali-shoper-v-podarok-ot-filtra-i-rasprodazha-v-outpac',

    'https://inde.io/article/6225-reviziya-devyat-kazanskih-sekond-hendov-iz-kotoryh-ne-uyti-s-pustymi-rukami',
    'https://inde.io/article/52590-ot-ked-do-tufel-13-rossiyskih-brendov-obuvi-dlya-vseh',
    'https://inde.io/article/2352-ugolok-potrebitelya-elochnye-igrushki-v-polka-market-novyy-kofeynyy-glintveyn-v-kafeteriuse-i-ochen-deshevaya-zubnaya-pasta-v-magnite',
    'https://inde.io/article/1918-eksperiment-redaktsiya-inde-testiruet-sluzhby-taksi',
    'https://inde.io/article/4657-ugolok-potrebitelya-vygodnyy-nochnoy-fitnes-v-maximus-skidki-na-syry-v-perekrestke-i-novaya-tochka-papa-dzhons-na-gorkah',
    'https://inde.io/article/71586-rabochiy-vopros-pr-menedzher-v-direktsiyu-po-razvitiyu-prirodnyh-territoriy-i-ekoturizma-shveya-v-my-nude-nymph-i-dizayner-prezentatsiy-v-yandeks',
    'https://inde.io/article/64235-rabochiy-vopros-prodzhekt-menedzher-v-agentstvo-500na700-dizayner-v-natsbiblioteku-rt-i-fotograf-na-proizvodstvo-svetilnikov',
    'https://inde.io/article/35486-rabochiy-vopros-dizayner-v-smenu-barmen-v-sol-i-rekruter-v-thesoul-publishing',
    'https://inde.io/article/9384-plany-na-posledniy-rabochiy-den-i-kanikuly-predstavleniya-remue-menage-i-vysokih-bratiev-kontserty-mubaya-i-chicherinoy-tri-novogodnie-vecherinki-i-chetyre-spektaklya',
    'https://inde.io/article/27458-igry-v-kotorye-igraet-redaktsiya-inde',
    'https://inde.io/article/43463-rabochiy-vopros-videooperator-v-natsionalnuyu-biblioteku-rt-barista-v-kunak-i-animator-v-soyuzmultpark',
    'https://inde.io/article/18291-rabochiy-vopros-korrespondent-stilist-dizayner-i-ofitsiant',
    'https://inde.io/article/47710-yasno-ponyatno-kak-zaveschat-svoi-telo-i-organy-nauke',
    'https://inde.io/article/1882-ugolok-potrebitelya-novosti-magazinov-i-restoranov-s-3-go-po-9-oktyabrya',
    'https://inde.io/article/18787-chto-smotret-i-vo-chto-igrat-pervaya-chast-vesennego-layfstayl-gida-inde',
    'https://inde.io/article/53649-rabochiy-vopros-menedzher-po-rabote-s-klientami-v-imagestudio-menedzher-v-direktsiyu-parkov-kazani-i-rukovoditel-proektov-v-ilar',
    'https://inde.io/article/14209-ugolok-potrebitelya-rasprodazha-v-outpac-sup-v-obmen-na-tsvety-v-foshnoy-i-pivo-za-99-rubley-v-pettsolde',
    'https://inde.io/article/46736-ugolok-potrebitelya-skidka-v-sole-fresh-rasprodazha-v-farfetch-i-aktsii-v-tyubetee',
    'https://inde.io/article/4573-yasno-ponyatno-chem-tatarstanu-grozit-holodnaya-vesna',
    'https://inde.io/article/21001-rabochiy-vopros-smm-menedzher-pekar-hr-spetsialist-i-hostes',
    'https://inde.io/article/912-gid-gde-pokupat-i-ne-pokupat-kulich-k-pashe'

]

# Папка для сохранения выкаченных страниц
output_dir = 'downloaded_pages'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

index_file = 'index.txt'

# Открываем файл для записи индекса
with open(index_file, 'w', encoding='utf-8') as index:
    for i, url in enumerate(urls, start=1):
        try:
            # Запрос к странице
            response = requests.get(url)
            response.raise_for_status()

            # Сохранение страницы в файл
            filename = os.path.join(output_dir, f'page_{i}.txt')
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(response.text)  # Сохраняем HTML с разметкой

            # Запись в индексный файл
            index.write(f'{i}: {url}\n')

            print(f'Страница {i} успешно скачана: {url}')
        except requests.RequestException as e:
            print(f'Ошибка при скачивании страницы {url}: {e}')

print('Все страницы скачаны.')