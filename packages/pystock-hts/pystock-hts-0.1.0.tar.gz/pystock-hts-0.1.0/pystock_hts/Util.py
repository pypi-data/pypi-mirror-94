def calculateCompoundInterest(seed_money: int, percent: int, after_date: int, end_date: int, after_date_type: str ="d", end_date_type: str ="d"):
  """
  복리 계산기 (seed_money 가 percent 만큼 after_date after_date_type 마다 이자가 발생할 때, end_date end_date_type 후에 금액은)
  """
  date_type_list = ["d", "w", "m", "y"]
  if not after_date_type in date_type_list or not end_date_type in date_type_list:
    raise Exception("param \'date_type\' is invalid")
  if not type(seed_money) == int or not type(percent) == int or not type(after_date) == int or not type(end_date) == int:
    raise Exception("params (seed_money, percent, after_date, end_date) Allowed only int type")
  
  after_day_count = after_date
  if after_date_type == "d":
    after_day_count = after_date * 1
  elif after_date_type == "w":
    after_day_count = after_date * 7
  elif after_date_type == "m":
    after_day_count = after_date * 30
  elif after_date_type == "y":
    after_day_count = after_date * 365
  
  end_day_count = end_date
  if after_date_type == "d":
    end_day_count = end_date * 1
  elif end_date_type == "w":
    end_day_count = end_date * 7
  elif end_date_type == "m":
    end_day_count = end_date * 30
  elif end_date_type == "y":
    end_day_count = end_date * 365
    
  
  iterval_time = int(end_day_count / after_day_count)
  for date in range(iterval_time):
    seed_money = seed_money + int(seed_money * (1/100))
    
  return seed_money

print(calculateCompoundInterest(1000000, 1, 2, 13, "m", "m"))
