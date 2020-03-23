s1 = """
>>> 2 + 2
4
>>> 50 - 5*6
20
>>> (50 - 5*6) / 4
5.0
>>> 8 / 5  # division always returns a floating point number
1.6
"""

s = """
>>> 17 / 3  # classic division returns a float
5.666666666666667
>>>
>>> 17 // 3  # floor division discards the fractional part
5
>>> 17 % 3  # the % operator returns the remainder of the division
2
>>> 5 * 3 + 2  # result * divisor + remainder
17
"""

s = s.replace(">>>", "")
a = s.split("\n")

a = [x.split('#')[0].strip() for x in a if x not in ['']]

# res = []
for r in a:
    print(r)
    # entities = []
    # while r:
    #     entities.append(
    #         {
    #             "entity"
    #         }
    #     )
    # e = {
    #     "text": f'return {r}',
    #     "intent": "return_statement",
    #     "entities": []
    # }
    # res.append(e)

"""
return 17 / 3
return 5.666666666666667
return 17 // 3
return 5
return 17 % 3
return 2
return 5 * 3 + 2
return 17
"""