from Currency import Currency


class Color:
   RED = '\033[91m'
   BOLD = '\033[1m'
   BOLD_END = '\033[0m'

class Color_telegram:
    RED = '\033[91m'
    BOLD = '*'
    BOLD_END = '*'


class CalculatedData:

    def exchange_rate_calculation_uzb(self, course):
        currency = Currency()
        color = Color_telegram()

        # Обновляем офиц данные
        currency.official_usd_rub = currency.str_to_float(currency.get_currency_price_google(currency.usd_rub))

        # собираем данные с банка ravnak
        list_ravnak = []
        list_ravnak.append(['sell', 'USD'])
        list_course = currency.ger_currency_price_ravnak(list_ravnak)
        sell_USD_ravnak = currency.str_to_float(list_course['USD_sell'])

        result = sell_USD_ravnak / course
        overpayment = currency.overpayment(result)
        formula = f"{str(sell_USD_ravnak)} / {str(course)}"
        description = f'\nКурс hggg через Узбекистан (Тинькофф): {color.BOLD}{round(result, 2)}{color.BOLD_END}. ({formula}) Переплата: {overpayment}%.'

        return description

    def exchange_rate_calculation(self):
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

        result["official_usd_rub"] = currency.official_usd_rub
        result["ISR_gc"] = currency.ger_currency_price_gold_crown('ISR')
        result["KGS_gc_rub"] = sell_USD_kicb / buy_rub_kicb

        kgs_rub = currency.get_currency_price_kursy_mir('Кыргызский сом')
        result["KGS_mir"] = currency.str_to_float(kgs_rub) * sell_USD_kicb

        kgz_rub = currency.ger_currency_price_gold_crown('KGZ')
        result["KGS_gc_usd"] = kgz_rub / buy_USD_kicb * sell_USD_kicb

        uzb_rub = currency.ger_currency_price_gold_crown('UZB')
        result["UZB_gc"] = uzb_rub / buy_USD_ravnak * sell_USD_ravnak

        usd_rub = currency.get_currency_price_bcs('buy', 'USD')
        bcs_swift1 = usd_rub * 1.02
        bcs_swift2 = bcs_swift1 * 1.01
        bcs_swift3 = bcs_swift1 * 1.005
        result["bcs_swift"] = {"bcs_swift1": bcs_swift1, "bcs_swift2": bcs_swift2, "bcs_swift3": bcs_swift3}

        return result

    def composing_message(self, result, this_telegram=False):
        currency = Currency()
        if this_telegram:
            color = Color_telegram()
        else:
            color = Color()

        description = {}
        description['official_usd_rub'] = f'Официальный курс usd к rub: {color.BOLD}(result){color.BOLD_END}.'
        description['ISR_gc'] = f'\n\nКурс через Израиль (ЗК): {color.BOLD}(result){color.BOLD_END}. Дополнительно будет комиссия при снятии. Переплата: (overpayment)%.'
        description['KGS_mir'] = f'\nКурс через Киргизию (МИР): {color.BOLD}(result){color.BOLD_END}. Переплата: (overpayment)%.'
        description['KGS_gc_usd'] = f'\nКурс через Киргизию (ЗК - usd): {color.BOLD}(result){color.BOLD_END}. Переплата: (overpayment)%.'
        description['KGS_gc_rub'] = f'\nКурс через Киргизию (ЗК - rub): {color.BOLD}(result){color.BOLD_END}. Переплата: (overpayment)%. Дополнительно комиссия короны 50 rub.'
        description['UZB_gc'] = f'\nКурс через Узбекистан (ЗК): {color.BOLD}(result){color.BOLD_END}. Переплата: (overpayment)%.'
        description['bcs_swift'] = f'\nКурс через БКС (свифт): {color.BOLD}(result1){color.BOLD_END}. Переплата: (overpayment1)%. Дополнительно комиссия 37.5 usd. ' \
                                   f'Если выводить 4000 usd, то курс: {color.BOLD}(result2){color.BOLD_END}. Переплата: (overpayment2)%. ' \
                                   f'Если выводить 8000 usd, то курс: {color.BOLD}(result3){color.BOLD_END}. Переплата: (overpayment3)%.'

        new_results = {}
        for key, value in result.items():
            if key == 'bcs_swift':
                new_result2 = {}
                for key2, value2 in value.items():
                    new_result2[key2] = {'result': round(value2, 2), 'overpayment': currency.overpayment(value2)}
                new_results[key] = new_result2
            else:
                new_results[key] = {'result': round(value, 2), 'overpayment': currency.overpayment(value)}

        final_text = ''
        for key, value in description.items():
            new_result = new_results[key]
            if key == 'bcs_swift':
                new_value = value.replace('(result1)', str(new_result['bcs_swift1']['result']))
                new_value = new_value.replace('(overpayment1)', str(new_result['bcs_swift1']['overpayment']))
                new_value = new_value.replace('(result2)', str(new_result['bcs_swift2']['result']))
                new_value = new_value.replace('(overpayment2)', str(new_result['bcs_swift2']['overpayment']))
                new_value = new_value.replace('(result3)', str(new_result['bcs_swift3']['result']))
                new_value = new_value.replace('(overpayment3)', str(new_result['bcs_swift3']['overpayment']))
            else:
                new_value = value.replace('(result)', str(new_result['result']))
                new_value = new_value.replace('(overpayment)', str(new_result['overpayment']))
            final_text += new_value

        return final_text