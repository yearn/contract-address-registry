from brownie import Contract, accounts, web3, chain, ZERO_ADDRESS
from pathlib import Path
import os
import json

def main():
    # pulled this from my ape-safe testing page, used for checking that address registry isn't compromised
    # fetch all of our vaults and strategies
    vaults_and_strategies = []
    yearn_registry = Contract("0x50c1a2eA0a861A967D9d0FFE2AE4012c2E053804")
    num_tokens = yearn_registry.numTokens()

    # iterate through the registry based on our length of tokens
    for number in range(num_tokens):
        token = yearn_registry.tokens(number)
        # check if we have multiple vaults for the same token
        num_vaults = yearn_registry.numVaults(token)
        # get all of the vaults
        for x in range(num_vaults):
            vault = yearn_registry.vaults(token, x)
            vaults_and_strategies.append(vault)
            vault_contract = Contract(vault)
            # print("This is our vault:", vault_contract.name(), "Version:", vault_contract.apiVersion())
            # get each strategy attached
            for strat_length in range(20):
                strategy = vault_contract.withdrawalQueue(strat_length)
                if strategy == ZERO_ADDRESS:
                    break
                else:
                    vaults_and_strategies.append(strategy)
                    # print("Strategy Address:", strategy)

    print("Number of addresses:", len(vaults_and_strategies))

    f = open(os.path.join(Path().resolve(), 'ethereum.json'))
    eth_addresses = json.load(f)
    eth_strategies = eth_addresses["strategies"]
    level_one = list(eth_strategies.keys())
    level_one_length = len(level_one)

    addresses_to_check = []
    level_four_addresses = []

    for first_number in range(level_one_length):
        # select a specific subgroup
        level_one_group = eth_strategies[level_one[first_number]]
        try:
            level_two = list(level_one_group.keys())
            level_two_length = len(level_two)
            for second_number in range(level_two_length):
                level_two_group = level_one_group[level_two[second_number]]
                try:
                    level_three = list(level_two_group.keys())
                    level_three_length = len(level_three)
                    for third_number in range(level_three_length):
                        level_three_group = level_two_group[level_three[third_number]]
                        try:
                            level_four = list(level_three_group.keys())
                            level_four_length = len(level_four)
                            level_four_addresses.append(level_four)
                        except:
                            print("Done with this, round three:", level_one[first_number], level_two[second_number], level_three[third_number])
                            addresses_to_check.append(level_three_group)
                except:
                    print("Done with this, round two:", level_one[first_number], level_two[second_number])
                    addresses_to_check.append(level_two_group)
        except:
            print("Done with this, round one:", level_one[first_number], "\n\n")
            addresses_to_check.append(eth_strategies[level_one[first_number]])

    eth_vaults = eth_addresses["vaults"]
    level_one = list(eth_vaults.keys())
    level_one_length = len(level_one)

    for first_number in range(level_one_length):
        # select a specific subgroup
        level_one_group = eth_vaults[level_one[first_number]]
        try:
            level_two = list(level_one_group.keys())
            level_two_length = len(level_two)
            for second_number in range(level_two_length):
                level_two_group = level_one_group[level_two[second_number]]
                try:
                    level_three = list(level_two_group.keys())
                    level_three_length = len(level_three)
                    for third_number in range(level_three_length):
                        level_three_group = level_two_group[level_three[third_number]]
                        try:
                            level_four = list(level_three_group.keys())
                            level_four_length = len(level_four)
                            level_four_addresses.append(level_four)
                        except:
                            print("Done with this, round three:", level_one[first_number], level_two[second_number], level_three[third_number])
                            addresses_to_check.append(level_three_group)
                except:
                    print("Done with this, round two:", level_one[first_number], level_two[second_number])
                    addresses_to_check.append(level_two_group)
        except:
            print("Done with this, round one:", level_one[first_number], "\n\n")
            addresses_to_check.append(eth_vaults[level_one[first_number]])

    print("Addresses:", addresses_to_check)
    assert level_four_addresses == []

    for x in addresses_to_check:
        try:
            assert x in vaults_and_strategies or x == ZERO_ADDRESS
        except:
            print("Address not found in registry:", x)
