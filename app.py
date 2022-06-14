from flask import Flask, render_template, request, redirect
from flask_login import login_required, current_user, LoginManager, UserMixin
from auth.auth import auth as auth_blueprint
from data_base import Database
from models import Product
from cloudipsp import Api, Checkout
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)
db = Database().connect()
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(email):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    # return User.query.get(int(user_id))
    return Database().check_user_exists(email=email)


app.register_blueprint(auth_blueprint)

products_list = [Product("5 фунтов 1966 год. Родезия. Золото 917 пробы - 40 грамм. Тираж 3000 шт. Редкость!",
                         166661,
                         1,
                         "https://static.auction.ru/offer_images/rd48/2022/05/30/03/small/5/5sK3rEpjx1P/zoloto_583_proby_sssr_prekrasnoe_azhurnoe_zolotoe_kolco_s_bolshim_jarkim_jantarem_zheltok.jpg"),
                 Product("Деньга 1805 ЕМ (R)  [561]",
                         37000,
                         2,
                         "https://static.auction.ru/offer_images/rd48/2022/04/03/10/small/N/n74dAig3bzP/as_denga_1805_em_r_561.jpg"),
                 Product("ЗОЛОТО 583 ПРОБЫ СССР!! ПРЕКРАСНОЕ АЖУРНОЕ ЗОЛОТОЕ КОЛЬЦО С БОЛЬШИМ, ЯРКИМ ЯНТАРЕМ ЖЕЛТОК",
                         29500,
                         3,
                         "https://static.auction.ru/offer_images/rd48/2022/05/30/03/small/5/5sK3rEpjx1P/zoloto_583_proby_sssr_prekrasnoe_azhurnoe_zolotoe_kolco_s_bolshim_jarkim_jantarem_zheltok.jpg"),
                 Product(
                         "2 КОПЕЙКИ 1927 СССР UNC СУПЕР (В ТАКОЙ СОХРАННОСТИ ТОЛЬКО В КОЛЛЕКЦИЯХ) ПРЕДЛОЖИТЕ ВАШУ ЦЕНУ У",
                         850000,
                         4,
                         "https://static.auction.ru/offer_images/rd48/2022/05/31/08/small/L/L9Zxra6ElGY/2_kopejki_1927_sssr_unc_super_v_takoj_sokhrannosti_tolko_v_kollekcijakh_predlozhite_vashu_cenu_u.jpg"),
                 Product("1995г 500000 рублей слаб PMG-66 EPQ (АП 1988935)",
                         160000,
                         5,
                         "https://static.auction.ru/offer_images/rd48/2022/05/04/10/small/A/a87QNnrE3Kx/1995_g_500000_rublej_slab_pmg_66_epq_ap_1988935.jpg"),
                 Product("5 копеек 1926 UNC MS63 NGC",
                         24500,
                         6,
                         "https://static.auction.ru/offer_images/rd48/2022/05/23/12/small/K/k62W3pWytTN/5_kopeek_1926_unc_ms63_ngc.jpg"),
                 Product(
                         "ЗОЛОТО 585 ПРОБЫ! ОХРАННЫЙ ПЕРСТЕНЬ С НЕБЕСНЫМ АКВАМАРИНОМ ИЗГОТОВЛЕННЫЙ МАСТЕРСКОЙ В.МИХАЙЛОВА!",
                         21555,
                         7,
                         "https://static.auction.ru/offer_images/rd48/2022/06/07/02/small/Q/qRvamW6mO2x/zoloto_585_proby_okhrannyj_persten_s_nebesnym_akvamarinom_izgotovlennyj_masterskoj_v_mikhajlova.jpg"),
                 Product(
                         "100 рублей 1993 год. Сохраним наш мир. Бурый медведь. Золото 999 пробы - 15.55 грамм. ММД. #84",
                         26500,
                         8,
                         "https://static.auction.ru/offer_images/rd48/2022/06/09/04/small/J/jXLxJPeKXvR/100_rublej_1993_god_sokhranim_nash_mir_buryj_medved_zoloto_999_proby_15_55_gramm_mmd_84.jpg"),
                 Product(
                         "1 рубль 1898 г (АГ) Памятник Императору Александру II Дворик Коллекционный экземпляр тираж 5 000 шт.",
                         99000,
                         9,
                         "https://static.auction.ru/offer_images/rd48/2022/06/06/08/small/T/tISYfl8eUg5/1_rubl_1898_g_ag_pamjatnik_imperatoru_aleksandru_ii_dvorik_kollekcionnyj_ekzempljar_tirazh_5_000_sht.jpg"),
                 Product(
                        "RRR!!!ЧУЧЕЛО ГИГАНТСКОЙ ЧЕРЕПАХИ \"ЛОГГЕРХЕНД\" С КУБЫ 1961-1962КАРИБСКИЙ КРИЗИС!!!ОРИГИНАЛ!!!",
                        3425,
                        10,
                        "https://static.auction.ru/offer_images/rd48/2022/05/13/04/small/C/cob2IwcTVpu/rrr_chuchelo_gigantskoj_cherepakhi_loggerkhend_s_kuby_1961_1962_karibskij_krizis_original.jpg"),
                 Product("2 соверена 1823 год. Золото 916 пробы. вес 16 грамм.Великобритания. RRR 1.2.425",
                         106000,
                         11,
                         "https://static.auction.ru/offer_images/rd48/2022/06/07/04/small/H/hq9J229IlkS/2_soverena_1823_god_zoloto_916_proby_ves_16_gramm_velikobritanija_rrr_1_2_425.jpg"),
                 Product("10 рублей 1909 года, золото",
                         90000,
                         12,
                         "https://static.auction.ru/offer_images/rd48/2022/06/06/05/small/V/vKSzxLe3vIn/10_rublej_1909_goda_zoloto.jpg")]


@app.route('/')
def index():
    return render_template('index2.html', status='Main Page', list_lots=products_list)


# @app.route('/profile')
# @login_required
# def profile():
#     return render_template('profile.html', name=current_user.name)


@app.route('/lot')
def lot():
    name = request.args.get('name', None)
    cost = request.args.get('cost', None)
    lot_id = request.args.get('id', None)
    image = request.args.get('image', None)
    print(cost, lot_id)
    return render_template('lot.html', name=name, cost=int(cost), id=lot_id, image=image, bid=round(int(cost) / 4))


@app.route('/buy/<int:lot_id>')
def item_buy(lot_id):
    item = products_list[lot_id-1]
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    print(item.cost)
    data = {
        "currency": "RUB",
        "amount": str(item.cost) + '00'
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


if __name__ == '__main__':
    app.run()
