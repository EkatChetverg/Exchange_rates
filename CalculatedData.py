from Currency import Currency


class Color:
   BOLD = '\033[1m'
   BOLD_END = '\033[0m'

class Color_telegram_herocu:
    BOLD = '*'
    BOLD_END = '*'

class Color_telegram_awd:
    BOLD = '<b>'
    BOLD_END = '</b>'

class CalculatedData:

    def exchange_rate_calculation_uzb(self, course):
        currency = Currency()
        color = Color_telegram_awd()

        # Обновляем офиц данные
        currency.official_usd_rub = currency.str_to_float(currency.get_currency_price_google(currency.usd_rub))

        # собираем данные с банка ravnak
        list_ravnak = []
        list_ravnak.append(['sell', 'USD'])
        list_course = currency.ger_currency_price_ravnak(list_ravnak)
        sell_USD_ravnak = currency.str_to_float(list_course['USD_sell'])

        usd_ils = currency.str_to_float(currency.get_currency_price_google(currency.usd_ils))

        result = sell_USD_ravnak / course
        overpayment = currency.overpayment(result)
        formula = f"{str(sell_USD_ravnak)} / {str(course)}"
        result_ils = usd_ils * result
        result_ils_with_percent = round(result_ils + result_ils * currency.percent_ravnak, 2)
        description = f'\nУзбекистан (Тинькофф): {color.BOLD}{round(result, 2)}{color.BOLD_END}. ' \
                      f'({formula}), {round(result_ils, 2)}₪, (с комиссией {result_ils_with_percent})₪. Переплата: {overpayment}%.'

        return description

    def exchange_rate_calculation(self, this_telegram=False):
        result = {}
        currency = Currency()

        # Обновляем офиц данные
        currency.official_usd_rub = currency.str_to_float(currency.get_currency_price_google(currency.usd_rub))

        # собираем данные с банка kicb
        list_kicb = []
        list_kicb.append(['sell', 'USD'])
        list_kicb.append(['buy', 'USD'])
        list_kicb.append(['buy', 'RUB'])
        list_course = currency.get_currency_price_kicb(list_kicb)
        sell_USD_kicb = currency.str_to_float(list_course['USD_sell'])
        buy_USD_kicb = currency.str_to_float(list_course['USD_buy'])
        buy_rub_kicb = currency.str_to_float(list_course['RUB_buy'])

        # собираем данные с банка ravnak
        list_ravnak = []
        list_ravnak.append(['sell', 'USD'])
        list_ravnak.append(['buy', 'USD'])
        list_course = currency.ger_currency_price_ravnak(list_ravnak)
        sell_USD_ravnak = currency.str_to_float(list_course['USD_sell'])
        buy_USD_ravnak = currency.str_to_float(list_course['USD_buy'])

        result["official_usd_rub"] = {"result": currency.official_usd_rub}
        usd_ils = currency.str_to_float(currency.get_currency_price_google(currency.usd_ils))
        result["official_usd_ils"] = {"result": usd_ils}

        ISR_gc = currency.ger_currency_price_gold_crown('ISR')
        ISR_gc_ils = ISR_gc * usd_ils
        result["ISR_gc"] = {"result": round(ISR_gc, 2),
                            "overpayment": currency.overpayment(ISR_gc),
                            "result_ils": round(ISR_gc_ils, 2),
                            "result_ils_with_percent": round(ISR_gc_ils + ISR_gc_ils * currency.percent_gold_crown, 2)}

        KGS_gc_rub = sell_USD_kicb / buy_rub_kicb
        KGS_gc_rub_ils = KGS_gc_rub * usd_ils
        result["KGS_gc_rub"] = {"result": round(KGS_gc_rub, 2),
                                "formula": f"({str(sell_USD_kicb)} / {str(buy_rub_kicb)})",
                                "overpayment": currency.overpayment(KGS_gc_rub),
                                "result_ils": round(KGS_gc_rub_ils, 2),
                                "result_ils_with_percent": round(KGS_gc_rub_ils + KGS_gc_rub_ils * currency.percent_kicb, 2)}

        kgs_rub = currency.get_currency_price_kursy_mir('Кыргызский сом')
        KGS_mir = currency.str_to_float(kgs_rub) * sell_USD_kicb
        KGS_mir_ils = KGS_mir * usd_ils
        result["KGS_mir"] = {"result": round(KGS_mir, 2),
                             "formula": f"({str(kgs_rub)} × {str(sell_USD_kicb)})",
                             "overpayment": currency.overpayment(KGS_mir),
                             "result_ils": round(KGS_mir_ils, 2),
                             "result_ils_with_percent": round(KGS_mir_ils + KGS_mir_ils * currency.percent_kicb, 2)}

        kgz_rub = currency.ger_currency_price_gold_crown('KGZ')
        KGS_gc_usd = kgz_rub / buy_USD_kicb * sell_USD_kicb
        KGS_gc_usd_ils = KGS_gc_usd * usd_ils
        result["KGS_gc_usd"] = {"result": round(KGS_gc_usd, 2),
                                "formula": f"({str(kgz_rub)} / {str(buy_USD_kicb)} × {str(sell_USD_kicb)})",
                                "overpayment": currency.overpayment(KGS_gc_usd),
                                "result_ils": round(KGS_gc_usd_ils, 2),
                                "result_ils_with_percent": round(KGS_gc_usd_ils + KGS_gc_usd_ils * currency.percent_kicb, 2)}

        uzb_rub = currency.ger_currency_price_gold_crown('UZB')
        UZB_gc = uzb_rub / buy_USD_ravnak * sell_USD_ravnak
        UZB_gc_ils = UZB_gc * usd_ils
        result["UZB_gc"] = {"result": round(UZB_gc, 2),
                            "formula": f"({str(uzb_rub)} / {str(buy_USD_ravnak)} × {str(sell_USD_ravnak)})",
                            "overpayment": currency.overpayment(UZB_gc),
                            "result_ils": round(UZB_gc_ils, 2),
                            "result_ils_with_percent": round(UZB_gc_ils + UZB_gc_ils * currency.percent_kicb, 2)}

        usd_rub = currency.get_currency_price_bcs('buy', 'USD')
        bcs_swift1 = usd_rub * 1.02
        bcs_swift2 = bcs_swift1 * 1.01
        bcs_swift3 = bcs_swift1 * 1.005
        result["bcs_swift"] = {"result1": round(bcs_swift1, 2), "formula1": f"({str(usd_rub)} × 1.02)", "overpayment1": currency.overpayment(bcs_swift1), "result_ils1": round(bcs_swift1 * usd_ils, 2),
                               "result2": round(bcs_swift2, 2), "formula2": f"({str(bcs_swift1)} × 1.01)", "overpayment2": currency.overpayment(bcs_swift2), "result_ils2": round(bcs_swift2 * usd_ils, 2),
                               "result3": round(bcs_swift3, 2), "formula3": f"({str(bcs_swift1)} × 1.005)", "overpayment3": currency.overpayment(bcs_swift3), "result_ils3": round(bcs_swift3 * usd_ils, 2)}

        final_text = self.composing_message(result, this_telegram)
        return final_text

    def composing_message(self, result, this_telegram):
        if this_telegram:
            color = Color_telegram_awd()
        else:
            color = Color()

        description = {}
        description['official_usd_rub'] = f'Официальный курс usd к rub: {color.BOLD}(result)${color.BOLD_END}.'
        description['official_usd_ils'] = f'\nОфициальный курс usd к ils: {color.BOLD}(result)₪{color.BOLD_END}.'
        description['ISR_gc'] = f'\n\nИзраиль (ЗК): {color.BOLD}(result)${color.BOLD_END}, (result_ils)₪, (с комиссией (result_ils_with_percent))₪. Дополнительно будет комиссия при снятии. Переплата: (overpayment)%.'
        description['KGS_mir'] = f'\nКиргизия (МИР): {color.BOLD}(result)${color.BOLD_END} (formula), (result_ils)₪, (с комиссией (result_ils_with_percent))₪. Переплата: (overpayment)%.'
        description['KGS_gc_usd'] = f'\nКиргизия (ЗК - usd): {color.BOLD}(result)${color.BOLD_END} (formula), (result_ils)₪, (с комиссией (result_ils_with_percent))₪. Переплата: (overpayment)%.'
        description['KGS_gc_rub'] = f'\nКиргизия (ЗК - rub): {color.BOLD}(result)${color.BOLD_END} (formula), (result_ils)₪, (с комиссией (result_ils_with_percent))₪. Переплата: (overpayment)%. Дополнительно комиссия короны 50 rub.'
        description['UZB_gc'] = f'\nУзбекистан (ЗК): {color.BOLD}(result)${color.BOLD_END} (formula), (result_ils)₪, (с комиссией (result_ils_with_percent))₪. Переплата: (overpayment)%.'
        description['bcs_swift'] = f'\nБКС (свифт): {color.BOLD}(result1)${color.BOLD_END} (formula1), (result_ils1)₪. Переплата: (overpayment1)%. Дополнительно комиссия 37.5 usd. ' \
                                   f'Если выводить 4000 usd, то курс: {color.BOLD}(result2)${color.BOLD_END} (formula2), (result_ils2)₪. Переплата: (overpayment2)%. ' \
                                   f'Если выводить 8000 usd, то курс: {color.BOLD}(result3)${color.BOLD_END} (formula3), (result_ils3)₪. Переплата: (overpayment3)%.'

        final_text = ''
        for key, value in description.items():
            new_result = result[key]
            new_value = value
            for key_result, value_result in new_result.items():
                new_value = new_value.replace(f'({key_result})', str(value_result))
            final_text += new_value

        return final_text

# cd = CalculatedData()
# usd_ils = cd.exchange_rate_calculation()
# print(usd_ils)