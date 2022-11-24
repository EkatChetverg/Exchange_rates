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
        description = f'\nУзбекистан (Тинькофф): {color.BOLD}{round(result, 2)}{color.BOLD_END}. ({formula}) Переплата: {overpayment}%.'

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

        result["official_usd_rub"] = {"result": currency.official_usd_rub, "formula": "", "overpayment": ""}

        ISR_gc = currency.ger_currency_price_gold_crown('ISR')
        result["ISR_gc"] = {"result": round(ISR_gc, 2), "formula": "", "overpayment": ""}

        KGS_gc_rub = sell_USD_kicb / buy_rub_kicb
        result["KGS_gc_rub"] = {"result": round(KGS_gc_rub, 2),
                                "formula": f"({str(sell_USD_kicb)} / {str(buy_rub_kicb)})",
                                "overpayment": currency.overpayment(KGS_gc_rub)}

        kgs_rub = currency.get_currency_price_kursy_mir('Кыргызский сом')
        KGS_mir = currency.str_to_float(kgs_rub) * sell_USD_kicb
        result["KGS_mir"] = {"result": round(KGS_mir, 2),
                             "formula": f"({str(kgs_rub)} * {str(sell_USD_kicb)})",
                             "overpayment": currency.overpayment(KGS_mir)}

        kgz_rub = currency.ger_currency_price_gold_crown('KGZ')
        KGS_gc_usd = kgz_rub / buy_USD_kicb * sell_USD_kicb
        result["KGS_gc_usd"] = {"result": round(KGS_gc_usd, 2),
                                "formula": f"({str(kgz_rub)} / {str(buy_USD_kicb)} * {str(sell_USD_kicb)})",
                                "overpayment": currency.overpayment(KGS_gc_usd)}

        uzb_rub = currency.ger_currency_price_gold_crown('UZB')
        UZB_gc = uzb_rub / buy_USD_ravnak * sell_USD_ravnak
        result["UZB_gc"] = {"result": round(UZB_gc, 2),
                            "formula": f"({str(uzb_rub)} / {str(buy_USD_ravnak)} * {str(sell_USD_ravnak)})",
                            "overpayment": currency.overpayment(UZB_gc)}

        usd_rub = currency.get_currency_price_bcs('buy', 'USD')
        bcs_swift1 = usd_rub * 1.02
        bcs_swift2 = bcs_swift1 * 1.01
        bcs_swift3 = bcs_swift1 * 1.005
        result["bcs_swift"] = {"result1": round(bcs_swift1, 2), "formula1": f"({str(usd_rub)} * 1.02)", "overpayment1": currency.overpayment(bcs_swift1),
                               "result2": round(bcs_swift2, 2), "formula2": f"({str(bcs_swift1)} * 1.01)", "overpayment2": currency.overpayment(bcs_swift2),
                               "result3": round(bcs_swift3, 2), "formula3": f"({str(bcs_swift1)} * 1.005)", "overpayment3": currency.overpayment(bcs_swift3)}

        final_text = self.composing_message(result, this_telegram)
        return final_text

    def composing_message(self, result, this_telegram):
        if this_telegram:
            color = Color_telegram()
        else:
            color = Color()

        description = {}
        description['official_usd_rub'] = f'Официальный курс usd к rub: {color.BOLD}(result){color.BOLD_END}.'
        description['ISR_gc'] = f'\n\nИзраиль (ЗК): {color.BOLD}(result){color.BOLD_END}. Дополнительно будет комиссия при снятии. Переплата: (overpayment)%.'
        description['KGS_mir'] = f'\nКиргизия (МИР): {color.BOLD}(result){color.BOLD_END} (formula). Переплата: (overpayment)%.'
        description['KGS_gc_usd'] = f'\nКиргизия (ЗК - usd): {color.BOLD}(result){color.BOLD_END} (formula). Переплата: (overpayment)%.'
        description['KGS_gc_rub'] = f'\nКиргизия (ЗК - rub): {color.BOLD}(result){color.BOLD_END} (formula). Переплата: (overpayment)%. Дополнительно комиссия короны 50 rub.'
        description['UZB_gc'] = f'\nУзбекистан (ЗК): {color.BOLD}(result){color.BOLD_END} (formula). Переплата: (overpayment)%.'
        description['bcs_swift'] = f'\nБКС (свифт): {color.BOLD}(result1){color.BOLD_END} (formula1). Переплата: (overpayment1)%. Дополнительно комиссия 37.5 usd. ' \
                                   f'Если выводить 4000 usd, то курс: {color.BOLD}(result2){color.BOLD_END} (formula2). Переплата: (overpayment2)%. ' \
                                   f'Если выводить 8000 usd, то курс: {color.BOLD}(result3){color.BOLD_END} (formula3). Переплата: (overpayment3)%.'

        final_text = ''
        for key, value in description.items():
            new_result = result[key]
            if key == 'bcs_swift':
                new_value = value.replace('(result1)', str(new_result['result1']))
                new_value = new_value.replace('(overpayment1)', str(new_result['overpayment1']))
                new_value = new_value.replace('(result2)', str(new_result['result2']))
                new_value = new_value.replace('(overpayment2)', str(new_result['overpayment2']))
                new_value = new_value.replace('(result3)', str(new_result['result3']))
                new_value = new_value.replace('(overpayment3)', str(new_result['overpayment3']))
                new_value = new_value.replace('(formula1)', new_result['formula1'])
                new_value = new_value.replace('(formula2)', new_result['formula2'])
                new_value = new_value.replace('(formula3)', new_result['formula3'])
            else:
                new_value = value.replace('(result)', str(new_result['result']))
                new_value = new_value.replace('(formula)', new_result['formula'])
                new_value = new_value.replace('(overpayment)', str(new_result['overpayment']))
            final_text += new_value

        return final_text