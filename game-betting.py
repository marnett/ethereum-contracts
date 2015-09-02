init:
    contract.storage[‘owner’] = msg.sender # owner address
    contract.storage[‘has_ended’] = 0 # whether betting has ended
    contract.storage[‘payoff_side1’] = msg.data[0] # payoff ratio; Ireland : 10
    contract.storage[‘payoff_side2’] = msg.data[1] # payoff ratio; India : 2
    contract.storage[‘buffer_money’] = msg.value # owner keeps some buffer money to pay to people
    contract.storage[‘numbetters’] = 0 # number of bets placed

    # compute total money that can be supported by this contract
    contract.storage[‘maxmoney_side1’] = contract.storage[‘buffer_money’] / contract.storage[‘payoff_side1’]
    contract.storage[‘maxmoney_side2’] = contract.storage[‘buffer_money’] / contract.storage[‘payoff_side2’]

    # total bets placed until now on either side
    contract.storage[‘betplaced_side1’] = 0
    contract.storage[‘betplaced_side2’] = 0
code:
  if (contract.storage[‘has_ended’] = 1):
	# bet has ended, sender gets the money back
	send(msg.sender, msg.value)
	return (0)

  # non owner sends a message, wants to bet
  elif ((msg.sender != contract.storage[‘owner’]) and (msg.datasize == 1)):
	if msg.data[0] == ‘side1’:
if contract.storage[‘betplaced_side1’] + msg.value > contract.storage[‘maxmoney_side1’]:
	send(msg.sender, msg.value)
	return (0)
elif msg.data[0] == ‘side2’:
if contract.storage[‘betplaced_side2’] + msg.value > contract.storage[‘maxmoney_side2’]:
	send(msg.sender, msg.value)
	return (0)
else:
send(msg.sender, msg.value)
return (0)
	contract.storage[3 * contract.storage[‘numbetters’] + 0] = msg.sender
	contract.storage[3 * contract.storage[‘numbetters’] + 1] = msg.data[0] # bet placed on
	contract.storage[3 * contract.storage[‘numbetters’] + 2] = msg.value # amount of bet
	contract.storage[‘numbetters’] = contract.storage[‘numbetters’] + 1
	if msg.data[0] == ‘side1’:
		contract.storage[‘betplaced_side1’] = contract.storage[‘betplaced_side1’] + msg.value
	else:
		contract.storage[‘betplaced_side2’] = contract.storage[‘betplaced_side2’] + msg.value
	return (1)

# end of the game, declare result and give money to winners.
elif (msg.sender == contract.storage[‘owner’]) and (msg.datasize ==1):
# data[0] is the winning side
     winning_payoff = 0
	if msg.data[0] == ‘side1’:
		winning_payoff = contract.storage[‘payoff_side1’]
	elif msg.data[0] == ‘side2’:
		winning_payoff = contract.storage[‘payoff_side2’]
	i = 0
	# send money to all winners
	while i < contract.storage[‘numbetters’]:
		# check if it was a winning bet
		if contract.storage[3 * i + 1] == msg.data[0]:
send(contract.storage[3 * i], contract.storage[3 * i + 2] * winning_payoff)
		i += 1
	contract.storage[‘has_ended’] = 1
	send(contract.storage[‘owner’], contract.balance)
	return (1)
   else:
	# wrong data format
  	send(msg.sender, msg.value)
return (0)