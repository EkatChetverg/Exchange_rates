from Currency import Currency


class Color:
    BOLD = '\033[1m'
    BOLD_END = '\033[0m'


class Color_telegram_awd:
    BOLD = '<b>'
    BOLD_END = '</b>'


class CalculatedData:

    def exchange_rate_calculation_uzb(self, course):
        currency = Currency()
        result = {}
        official_result = {}

        # Обновляем офиц данные
        official_result["official_usd_rub"] = currency.get_currency_price_usd_rub()

        # собираем данные с банка ravnak
        list_ravnak = []
        list_ravnak.append(['sell', 'USD'])
        list_course = currency.ger_currency_price_ravnak(list_ravnak)
        sell_USD_ravnak = currency.str_to_float(list_course['USD_sell'])

        usd_ils = currency.get_currency_price_google(currency.usd_ils)
        official_result["official_usd_ils"] = usd_ils

        name_of_column = {"name": "Name of way",
                          "result": "Total ",
                          "result_ils": "Total ",
                          "overpayment": "Overpayment %",
                          "formula": "Formula $",
                          "formula_ils": "Formula ₪"}

        result_usd = sell_USD_ravnak / course
        result_usd_text = round(result_usd, 2)
        result_ils = result_usd / usd_ils * (currency.percent_ravnak1 + currency.percent_ravnak2)
        result_ils_text = round(result_ils, 2)
        result["UZB_tink"] = {"result": result_usd_text,
                              "result_ils": result_ils_text,
                              "name": "Uzbekistan (Tinkoff)",
                              "overpayment": f'{currency.overpayment(result_usd)}%',
                              "formula": f'{result_usd_text}$ = {str(sell_USD_ravnak)} / {str(course)}',
                              "formula_ils": f'{result_ils_text}₪ = {result_usd_text} / {usd_ils} * ({str(currency.percent_ravnak1)} + {str(currency.percent_ravnak2)})'}

        final_text = self.composing_message(official_result, name_of_column, result, True)

        return final_text

    def exchange_rate_calculation(self, full_calculations=False, this_telegram=False):
        result = {}
        official_result = {}
        currency = Currency()

        # Обновляем офиц данные
        currency.official_usd_rub = currency.get_currency_price_usd_rub()

        # собираем данные с банка kicb
        list_kicb = []
        list_kicb.append(['sell', 'USD'])
        list_kicb.append(['buy', 'USD'])
        list_kicb.append(['buy', 'RUB'])
        list_course = currency.get_currency_price_kicb(list_kicb)
        sell_USD_kicb = currency.str_to_float(list_course['USD_sell'])
        # buy_USD_kicb = currency.str_to_float(list_course['USD_buy'])
        buy_rub_kicb = currency.str_to_float(list_course['RUB_buy'])

        # собираем данные с банка ravnak
        list_ravnak = []
        list_ravnak.append(['sell', 'USD'])
        list_ravnak.append(['buy', 'USD'])
        list_course = currency.ger_currency_price_ravnak(list_ravnak)
        sell_USD_ravnak = currency.str_to_float(list_course['USD_sell'])
        buy_USD_ravnak = currency.str_to_float(list_course['USD_buy'])

        official_result["official_usd_rub"] = currency.official_usd_rub
        usd_ils = currency.get_currency_price_google(currency.usd_ils)
        official_result["official_usd_ils"] = usd_ils

        name_of_column = {"name": "Name of way",
                          "result": "Total ",
                          "result_ils": "Total "}

        ISR_gc = currency.ger_currency_price_gold_crown('ISR')
        ISR_gc_ils = ISR_gc / usd_ils
        result["ISR_gc"] = {"result": round(ISR_gc, 2),
                            "result_ils": round(ISR_gc_ils * currency.percent_gold_crown, 2),
                            "name": "Israel (GC)"}

        KGS_gc_rub = sell_USD_kicb / buy_rub_kicb * 1.005
        KGS_gc_rub_ils = KGS_gc_rub / usd_ils
        result["KGS_gc_rub"] = {"result": round(KGS_gc_rub, 2),
                                "result_ils": round(KGS_gc_rub_ils * currency.percent_kicb, 2),
                                "name": "Kyrgyzstan (GC rub)"}

        # kgs_rub = currency.str_to_float(currency.get_currency_price_kursy_mir('Кыргызский сом'))
        # KGS_mir = kgs_rub * sell_USD_kicb
        # KGS_mir_ils = KGS_mir / usd_ils
        # result["KGS_mir"] = {"result": round(KGS_mir, 2),
        #                      "result_ils": round(KGS_mir_ils * currency.percent_kicb, 2),
        #                      "name": "Kyrgyzstan (mir)"}

        # kgz_rub = currency.ger_currency_price_gold_crown('KGZ')
        # KGS_gc_usd = kgz_rub / buy_USD_kicb * sell_USD_kicb
        # KGS_gc_usd_ils = KGS_gc_usd / usd_ils
        # result["KGS_gc_usd"] = {"result": round(KGS_gc_usd, 2),
        #                         "result_ils": round(KGS_gc_usd_ils * currency.percent_kicb, 2),
        #                         "name": "Kyrgyzstan (GC usd)"}

        freedom_finance = currency.official_usd_rub * 1.004 * 1.01
        freedom_finance_ils = freedom_finance / usd_ils * 1.02
        result["freedom_finance"] = {"result": round(freedom_finance, 2),
                                    "result_ils": round(freedom_finance_ils, 2),
                                    "name": "Freedom finance"}

        binance = currency.get_currency_price_binance()
        binance_ils = binance / usd_ils
        result["binance"] = {"result": round(binance, 2),
                             "result_ils": round(binance_ils, 2),
                             "name": "Binance"}

        uzb_rub = currency.ger_currency_price_gold_crown('UZB')
        UZB_gc = uzb_rub / buy_USD_ravnak * sell_USD_ravnak
        UZB_gc_ils = UZB_gc / usd_ils
        result["UZB_gc"] = {"result": round(UZB_gc, 2),
                            "result_ils": round(UZB_gc_ils * (currency.percent_ravnak1 + currency.percent_ravnak2), 2),
                            "name": "Uzbekistan (GC)"}

        bcs_usd_rub = currency.get_currency_price_bcs('buy', 'USD')
        bcs_swift1 = bcs_usd_rub * 1.02
        bcs_swift1_ils = round(bcs_swift1 / usd_ils, 2)
        result["bcs_swift1"] = {"result": round(bcs_swift1, 2),
                                "result_ils": bcs_swift1_ils,
                                "name": "Bcs swift"}

        # bcs_swift2 = bcs_usd_rub * 1.01
        # bcs_swift2_ils = round(bcs_swift2 / usd_ils, 2)
        # result["bcs_swift2"] = {"result": round(bcs_swift2, 2),
        #                         "result_ils": bcs_swift2_ils,
        #                         "name": "Bcs swift (4000)"}
        #
        # bcs_swift3 = bcs_usd_rub * 1.005
        # bcs_swift3_ils = round(bcs_swift3 / usd_ils, 2)
        # result["bcs_swift3"] = {"result": round(bcs_swift3, 2),
        #                         "result_ils": bcs_swift3_ils,
        #                         "name": "Bcs swift (8000)"}

        if full_calculations:
            additional_information = {"usd_ils": str(usd_ils),
                                      # "kgs_rub": str(kgs_rub),
                                      # "kgz_rub": str(kgz_rub),
                                      "uzb_rub": str(uzb_rub),
                                      "bcs_usd_rub": str(bcs_usd_rub),
                                      "sell_USD_kicb": str(sell_USD_kicb),
                                      "buy_rub_kicb": str(buy_rub_kicb),
                                      # "buy_USD_kicb": str(buy_USD_kicb),
                                      "buy_USD_ravnak": str(buy_USD_ravnak),
                                      "sell_USD_ravnak": str(sell_USD_ravnak)}
            self.exchange_rate_calculation_full(name_of_column, result, additional_information)

        final_text = self.composing_message(official_result, name_of_column, result, this_telegram)
        return final_text

    def exchange_rate_calculation_full(self, name_of_column, result, additional_information):
        currency = Currency()

        name_of_column["overpayment"] = "Overpayment %"
        name_of_column["formula"] = "Formula $"
        name_of_column["formula_ils"] = "Formula ₪"

        result["ISR_gc"]["overpayment"] = f'{currency.overpayment(result["ISR_gc"]["result"])}%'
        result["ISR_gc"]["formula"] = f'{result["ISR_gc"]["result"]}$ = данные с ЗК'
        result["ISR_gc"]["formula_ils"] = f'{result["ISR_gc"]["result_ils"]}₪ = {result["ISR_gc"]["result"]} / {additional_information["usd_ils"]} * {str(currency.percent_gold_crown)}'

        result["KGS_gc_rub"]["overpayment"] = f'{currency.overpayment(result["KGS_gc_rub"]["result"])}%'
        result["KGS_gc_rub"]["formula"] = f'{result["KGS_gc_rub"]["result"]}$ = {additional_information["sell_USD_kicb"]} / {additional_information["buy_rub_kicb"]} * 1.005'
        result["KGS_gc_rub"]["formula_ils"] = f'{result["KGS_gc_rub"]["result_ils"]}₪ = {result["KGS_gc_rub"]["result"]} / {additional_information["usd_ils"]} * {str(currency.percent_kicb)}'

        # result["KGS_mir"]["overpayment"] = f'{currency.overpayment(result["KGS_mir"]["result"])}%'
        # result["KGS_mir"]["formula"] = f'{result["KGS_mir"]["result"]}$ = {additional_information["kgs_rub"]} * {additional_information["sell_USD_kicb"]}'
        # result["KGS_mir"]["formula_ils"] = f'{result["KGS_mir"]["result_ils"]}₪ = {result["KGS_mir"]["result"]} / {additional_information["usd_ils"]} * {str(currency.percent_kicb)}'

        # result["KGS_gc_usd"]["overpayment"] = f'{currency.overpayment(result["KGS_gc_usd"]["result"])}%'
        # result["KGS_gc_usd"]["formula"] = f'{result["KGS_gc_usd"]["result"]}$ = {additional_information["kgz_rub"]} / {additional_information["buy_USD_kicb"]} * {additional_information["sell_USD_kicb"]}'
        # result["KGS_gc_usd"]["formula_ils"] = f'{result["KGS_gc_usd"]["result_ils"]}₪ = {result["KGS_gc_usd"]["result"]} / {additional_information["usd_ils"]} * {str(currency.percent_kicb)}'

        result["freedom_finance"]["overpayment"] = f'{currency.overpayment(result["freedom_finance"]["result"])}%'
        result["freedom_finance"]["formula"] = f'{result["freedom_finance"]["result"]}$ = {currency.official_usd_rub} * 1.004 * 1.01'
        result["freedom_finance"]["formula_ils"] = f'{result["freedom_finance"]["result_ils"]}₪ = {result["freedom_finance"]["result"]} / {additional_information["usd_ils"]} * 1.02'

        result["binance"]["overpayment"] = f'{currency.overpayment(result["binance"]["result"])}%'
        result["binance"]["formula"] = f'{result["binance"]["result"]}$ = данные с binance'
        result["binance"]["formula_ils"] = f'{result["binance"]["result_ils"]}₪ = {result["binance"]["result"]} / {additional_information["usd_ils"]}'

        result["UZB_gc"]["overpayment"] = f'{currency.overpayment(result["UZB_gc"]["result"])}%'
        result["UZB_gc"]["formula"] = f'{result["UZB_gc"]["result"]}$ = {additional_information["uzb_rub"]} / {additional_information["buy_USD_ravnak"]} * {additional_information["sell_USD_ravnak"]}'
        result["UZB_gc"]["formula_ils"] = f'{result["UZB_gc"]["result_ils"]}₪ = {result["UZB_gc"]["result"]} / {additional_information["usd_ils"]} * ({str(currency.percent_ravnak1)} + {str(currency.percent_ravnak2)})'

        result["bcs_swift1"]["overpayment"] = f'{currency.overpayment(result["bcs_swift1"]["result"])}%'
        result["bcs_swift1"]["formula"] = f'{result["bcs_swift1"]["result"]}$ = {additional_information["bcs_usd_rub"]} * 1.02'
        result["bcs_swift1"]["formula_ils"] = f'{result["bcs_swift1"]["result_ils"]}₪ = {result["bcs_swift1"]["result"]} / {additional_information["usd_ils"]} (+ 37.5$)'

        # result["bcs_swift2"]["overpayment"] = f'{currency.overpayment(result["bcs_swift2"]["result"])}%'
        # result["bcs_swift2"]["formula"] = f'{result["bcs_swift2"]["result"]}$ = {additional_information["bcs_usd_rub"]} * 1.01'
        # result["bcs_swift2"]["formula_ils"] = f'{result["bcs_swift2"]["result_ils"]}₪ = {result["bcs_swift2"]["result"]} / {additional_information["usd_ils"]} + 37.5$'
        #
        # result["bcs_swift3"]["overpayment"] = f'{currency.overpayment(result["bcs_swift3"]["result"])}%'
        # result["bcs_swift3"]["formula"] = f'{result["bcs_swift3"]["result"]}$ = {additional_information["bcs_usd_rub"]} * 1.005'
        # result["bcs_swift3"]["formula_ils"] = f'{result["bcs_swift3"]["result_ils"]}₪ = {result["bcs_swift3"]["result"]} / {additional_information["usd_ils"]} + 37.5$'


    def row_formation(self, this_telegram, name_of_column, list_of_value=None):
        color = Color_telegram_awd() if this_telegram else Color()

        final_text = ""

        header1 = '\n'
        header2 = ''
        for key, value in name_of_column.items():
            meaning = value if list_of_value is None else list_of_value[key]
            if key == "name" or key == "result" or key == "result_ils":
                row_wd = 17 if key == "name" else 7
                currency = '$' if key == "result" else '₪' if key == "result_ils" else ''
                header1 += f'{color.BOLD}{str(meaning) + currency:{row_wd}s}{color.BOLD_END}|'
            else:
                header2 += f'\n{str(meaning)}'
        final_text += header1[:-1]
        final_text += header2

        return final_text

    def composing_message(self, official_result, name_of_column, result, this_telegram):
        color = Color_telegram_awd() if this_telegram else Color()

        final_text = f'Usd to rub: {color.BOLD}{official_result["official_usd_rub"]}${color.BOLD_END}.' \
                     f'\nUsd to ils: {color.BOLD}{official_result["official_usd_ils"]}₪{color.BOLD_END}. \n'

        fencing = ('-' * 40)

        final_text += fencing
        final_text += self.row_formation(this_telegram, name_of_column)
        final_text += '\n' + fencing

        for value in result.values():
            final_text += self.row_formation(this_telegram, name_of_column, value)
            final_text += '\n' + fencing

        return final_text


cd = CalculatedData()
usd_ils = cd.exchange_rate_calculation(True)
# usd_ils = cd.exchange_rate_calculation_uzb(171)
print(usd_ils)

