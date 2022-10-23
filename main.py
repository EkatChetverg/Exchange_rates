from CalculatedData import CalculatedData


def exchange_rate_calculation():
    calculatedData = CalculatedData()
    result_courses = calculatedData.exchange_rate_calculation()
    final_text = calculatedData.composing_message(result_courses)
    print(final_text)


if __name__ == '__main__':
    exchange_rate_calculation()
