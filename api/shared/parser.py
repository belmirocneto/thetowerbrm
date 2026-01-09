import re
from datetime import datetime
from decimal import Decimal


def parse_battle_report(raw_data):
    """
    Parse do Battle Report text para dicionário (suporta EN e PT-BR)
    """
    try:
        data = {}

        # Conversão de sufixos para números
        def parse_number(value_str):
            if not value_str or value_str == '0':
                return Decimal('0')

            value_str = value_str.replace('$', '').strip()
            value_str = value_str.replace(',', '.')

            suffixes = {
                'K': 1e3,
                'M': 1e6,
                'B': 1e9,
                'T': 1e12,
                'q': 1e15,
                'Q': 1e18,
                's': 1e21,
                'S': 1e24,
                'D': 1e27,
                'N': 1e30,
            }

            for suffix, multiplier in suffixes.items():
                if value_str.endswith(suffix):
                    number = float(value_str[:-1])
                    return Decimal(str(number * multiplier))

            try:
                value_str = value_str.replace('x', '')
                return Decimal(value_str)
            except:
                return Decimal('0')

        def get_field(pattern, default=None):
            match = re.search(pattern, raw_data, re.IGNORECASE | re.MULTILINE)
            return match.group(1).strip() if match else default

        # Battle Date - suporta EN e PT-BR
        date_str = get_field(r'(?:Battle Date|Data da Batalha)\s+(.+?)(?:\n|$)')
        if date_str:
            try:
                months = {
                    'jan': 'Jan', 'fev': 'Feb', 'feb': 'Feb', 'mar': 'Mar',
                    'abr': 'Apr', 'apr': 'Apr', 'mai': 'May', 'may': 'May',
                    'jun': 'Jun', 'jul': 'Jul', 'ago': 'Aug', 'aug': 'Aug',
                    'set': 'Sep', 'sep': 'Sep', 'out': 'Oct', 'oct': 'Oct',
                    'nov': 'Nov', 'dez': 'Dec', 'dec': 'Dec'
                }
                for pt, en in months.items():
                    date_str = date_str.replace(pt, en)

                data['battle_date'] = datetime.strptime(date_str, '%b %d, %Y %H:%M')
            except Exception as e:
                print(f"Erro ao parsear data: {e}")
                data['battle_date'] = datetime.now()
        else:
            data['battle_date'] = datetime.now()

        # Informações básicas - EN e PT-BR
        data['game_time'] = get_field(r'(?:Game Time|Tempo de Jogo)\s+(.+?)(?:\n|$)')
        data['real_time'] = get_field(r'(?:Real Time|Tempo Real)\s+(.+?)(?:\n|$)')
        data['tier'] = int(get_field(r'(?:Tier|Grau)\s+(\d+)', '0'))
        data['wave'] = int(get_field(r'(?:Wave|Onda)\s+(\d+)', '0'))
        data['killed_by'] = get_field(r'(?:Killed By|Morto por)\s+(.+?)(?:\n|$)', 'Unknown')

        # Coins e recursos
        data['coins_earned'] = parse_number(get_field(r'(?:Coins earned|Moedas ganhas)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['coins_per_hour'] = parse_number(get_field(r'(?:Coins per hour|Moedas por h)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['cash_earned'] = parse_number(get_field(r'(?:Cash earned|Dinheiro ganho)\s+\$?([\d,.]+[KMBTQSDN]?)', '0'))
        data['interest_earned'] = parse_number(
            get_field(r'(?:Interest earned|Juros ganhos)\s+\$?([\d,.]+[KMBTQSDN]?)', '0'))
        data['gem_blocks_tapped'] = int(get_field(r'(?:Gem Blocks Tapped|Blocos de Joias Tocados)\s+(\d+)', '0'))
        data['cells_earned'] = parse_number(get_field(r'(?:Cells Earned|Células Ganhas)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['reroll_shards_earned'] = parse_number(
            get_field(r'(?:Reroll Shards Earned|Fragmentos de Variação Obtidos)\s+([\d,.]+[KMBTQSDN]?)', '0'))

        # Combat
        data['damage_dealt'] = parse_number(get_field(r'(?:Damage dealt|Dano causado)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['damage_taken'] = parse_number(
            get_field(r'(?:Damage Taken|Dano Sofrido)(?!\s+(?:Wall|\(Wall\)|pelo Muro|Durante))\s+([\d,.]+[KMBTQSDN]?)',
                      '0'))
        data['damage_taken_wall'] = parse_number(
            get_field(r'(?:Damage Taken Wall|Damage Taken \(Wall\)|Dano Sofrido pelo Muro)\s+([\d,.]+[KMBTQSDN]?)',
                      '0'))
        data['damage_taken_while_berserked'] = parse_number(
            get_field(r'(?:Damage Taken While Berserked|Dano Sofrido Durante Fúria)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['damage_gain_from_berserk'] = parse_number(
            get_field(r'(?:Damage Gain From Berserk|Dano Ganho da Fúria)\s+[x]?([\d,.]+[KMBTQSDN]?)', '0'))
        data['death_defy'] = int(get_field(r'(?:Death Defy|Afronta à Morte)\s+(\d+)', '0'))
        data['lifesteal'] = parse_number(get_field(r'(?:Lifesteal|Roubo de Vida)\s+([\d,.]+[KMBTQSDN]?)', '0'))

        # Damage types
        data['projectiles_damage'] = parse_number(
            get_field(r'(?:Projectiles Damage|Dano de Projéteis)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['projectiles_count'] = parse_number(
            get_field(r'(?:Projectiles Count|Contagem de Projéteis)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['thorn_damage'] = parse_number(get_field(r'(?:Thorn damage|Dano de espinhos)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['orb_damage'] = parse_number(get_field(r'(?:Orb Damage|Dano de Orbe)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['enemies_hit_by_orbs'] = parse_number(
            get_field(r'(?:Enemies Hit by Orbs|Inimigos Atingidos por Orbes)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['land_mine_damage'] = parse_number(
            get_field(r'(?:Land Mine Damage|Dano da Mina Terrestre)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['land_mines_spawned'] = int(
            get_field(r'(?:Land Mines Spawned|Minas Terrestres Geradas)\s+([\d,]+)', '0').replace(',', '').replace('.',
                                                                                                                   ''))
        data['rend_armor_damage'] = parse_number(
            get_field(r'(?:Rend Armor Damage|Dano de Despedaçar Armadura)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['death_ray_damage'] = parse_number(
            get_field(r'(?:Death Ray Damage|Dano de Raio da Morte)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['smart_missile_damage'] = parse_number(
            get_field(r'(?:Smart Missile Damage|Dano de Mísseis Inteligentes)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['inner_land_mine_damage'] = parse_number(
            get_field(r'(?:Inner Land Mine Damage|Dano de Minas Terrestres Internas)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['chain_lightning_damage'] = parse_number(
            get_field(r'(?:Chain Lightning Damage|Dano de Relâmpago em Cadeia)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['death_wave_damage'] = parse_number(
            get_field(r'(?:Death Wave Damage|Dano de Onda da Morte)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['tagged_by_deathwave'] = int(
            get_field(r'(?:Tagged by Deathwave|Afetado por Onda da Morte)\s+([\d,]+)', '0').replace(',', '').replace(
                '.', ''))
        data['swamp_damage'] = parse_number(get_field(r'(?:Swamp Damage|Dano de Pântano)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['black_hole_damage'] = parse_number(
            get_field(r'(?:Black Hole Damage|Dano de Buraco Negro)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['electrons_damage'] = parse_number(
            get_field(r'(?:Electrons Damage|Danos causados por elétrons)\s+([\d,.]+[KMBTQSDN]?)', '0'))

        # Utility
        data['waves_skipped'] = int(
            get_field(r'(?:Waves Skipped|Ondas Puladas)\s+([\d,]+)', '0').replace(',', '').replace('.', ''))
        data['recovery_packages'] = int(
            get_field(r'(?:Recovery Packages|Pacotes de Recuperação)\s+([\d,]+)', '0').replace(',', '').replace('.',
                                                                                                                ''))
        data['free_attack_upgrade'] = int(
            get_field(r'(?:Free Attack Upgrade|Melhoria de Ataque Gratuita)\s+([\d,]+)', '0').replace(',', '').replace(
                '.', ''))
        data['free_defense_upgrade'] = int(
            get_field(r'(?:Free Defense Upgrade|Melhoria de Defesa Gratuita)\s+([\d,]+)', '0').replace(',', '').replace(
                '.', ''))
        data['free_utility_upgrade'] = int(
            get_field(r'(?:Free Utility Upgrade|Melhoria de Utilidade Gratuita)\s+([\d,]+)', '0').replace(',',
                                                                                                          '').replace(
                '.', ''))
        data['hp_from_death_wave'] = parse_number(
            get_field(r'(?:HP From Death Wave|HP da Onda da Morte)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['coins_from_death_wave'] = parse_number(
            get_field(r'(?:Coins From Death Wave|Moedas da Onda da Morte)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['cash_from_golden_tower'] = parse_number(
            get_field(r'(?:Cash From Golden Tower|Dinheiro da Torre Dourada)\s+\$?([\d,.]+[KMBTQSDN]?)', '0'))
        data['coins_from_golden_tower'] = parse_number(
            get_field(r'(?:Coins From Golden Tower|Moedas da Torre Dourada)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['coins_from_black_hole'] = parse_number(
            get_field(r'(?:Coins From Black Hole|Moedas do Buraco Negro)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['coins_from_spotlight'] = parse_number(
            get_field(r'(?:Coins From Spotlight|Moedas do Holofote)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['coins_from_orb'] = parse_number(
            get_field(r'(?:Coins From Orb|Moedas de Orbes)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['coins_from_coin_upgrade'] = parse_number(
            get_field(r'(?:Coins from Coin Upgrade|Moedas da Melhoria de Moeda)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['coins_from_coin_bonuses'] = parse_number(
            get_field(r'(?:Coins from Coin Bonuses|Moedas dos Bônus de Moeda)\s+([\d,.]+[KMBTQSDN]?)', '0'))

        # Enemies
        data['total_enemies'] = int(
            get_field(r'(?:Total Enemies|Total de Inimigos)\s+([\d,]+)', '0').replace(',', '').replace('.', ''))
        data['basic_enemies'] = int(get_field(r'(?:Basic|Básico)\s+([\d,]+)', '0').replace(',', '').replace('.', ''))
        data['fast_enemies'] = int(get_field(r'(?:Fast|Rápido)\s+([\d,]+)', '0').replace(',', '').replace('.', ''))
        data['tank_enemies'] = int(get_field(r'(?:Tank|Tanque)\s+([\d,]+)', '0').replace(',', '').replace('.', ''))
        data['ranged_enemies'] = int(
            get_field(r'(?:Ranged|Atirador)\s+([\d,]+)', '0').replace(',', '').replace('.', ''))
        data['boss_enemies'] = int(get_field(r'(?:Boss|Chefe)\s+([\d,]+)', '0').replace(',', '').replace('.', ''))
        data['protector_enemies'] = int(
            get_field(r'(?:Protector|Protetor)\s+([\d,]+)', '0').replace(',', '').replace('.', ''))
        data['total_elites'] = int(
            get_field(r'(?:Total Elites|Total de Elite)\s+([\d,]+)', '0').replace(',', '').replace('.', ''))
        data['vampires'] = int(get_field(r'(?:Vampires|Vampiros)\s+([\d,]+)', '0').replace(',', '').replace('.', ''))
        data['rays'] = int(get_field(r'(?:Rays|Raios)\s+([\d,]+)', '0').replace(',', '').replace('.', ''))
        data['scatters'] = int(
            get_field(r'(?:Scatters|Espalhamentos)\s+([\d,]+)', '0').replace(',', '').replace('.', ''))
        data['saboteur'] = int(get_field(r'(?:Saboteur|Sabotador)\s+([\d,]+)', '0').replace(',', '').replace('.', ''))
        data['commander'] = int(
            get_field(r'(?:Commander|Comandante)\s+([\d,]+)', '0').replace(',', '').replace('.', ''))
        data['overcharge'] = int(
            get_field(r'(?:Overcharge|Sobrecarga)\s+([\d,]+)', '0').replace(',', '').replace('.', ''))

        # Destroyed by
        data['destroyed_by_orbs'] = int(
            get_field(r'(?:Destroyed By Orbs|Destruído por Orbes)\s+([\d,]+)', '0').replace(',', '').replace('.', ''))
        data['destroyed_by_thorns'] = int(
            get_field(r'(?:Destroyed by Thorns|Destruído por Espinhos)\s+([\d,]+)', '0').replace(',', '').replace('.',
                                                                                                                  ''))
        data['destroyed_by_death_ray'] = int(
            get_field(r'(?:Destroyed by Death Ray|Destruído por Raio da Morte)\s+([\d,]+)', '0').replace(',',
                                                                                                         '').replace(
                '.', ''))
        data['destroyed_by_land_mine'] = int(
            get_field(r'(?:Destroyed by Land Mine|Destruído por Mina Terrestre)\s+([\d,]+)', '0').replace(',',
                                                                                                          '').replace(
                '.', ''))
        data['destroyed_in_spotlight'] = int(
            get_field(r'(?:Destroyed in Spotlight|Destruído no Holofote)\s+([\d,]+)', '0').replace(',', '').replace('.',
                                                                                                                    ''))

        # Bots
        data['flame_bot_damage'] = parse_number(
            get_field(r'(?:Flame Bot Damage|Dano do Bot de Fogo)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['thunder_bot_stuns'] = int(
            get_field(r'(?:Thunder Bot Stuns|Atordoamentos do Bot de Raio)\s+([\d,]+)', '0').replace(',', '').replace(
                '.', ''))
        data['golden_bot_coins_earned'] = parse_number(
            get_field(r'(?:Golden Bot Coins Earned|Moedas Recebidas do Bot Dourado)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['destroyed_in_golden_bot'] = int(
            get_field(r'(?:Destroyed in Golden Bot|Destruído por Bot Dourado)\s+([\d,]+)', '0').replace(',',
                                                                                                        '').replace('.',
                                                                                                                    ''))

        # Guardian
        data['guardian_damage'] = parse_number(
            get_field(r'(?:Guardian\s+)?(?:Damage|Dano)(?!\s+(?:dealt|causado|Sofrido|Taken))\s+([\d,.]+[KMBTQSDN]?)',
                      '0'))
        data['summoned_enemies'] = parse_number(
            get_field(r'(?:Summoned enemies|Inimigos invocados)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['guardian_coins_stolen'] = parse_number(
            get_field(r'(?:Guardian coins stolen|Moedas roubadas pelo guardião)\s+([\d,.]+[KMBTQSDN]?)', '0'))

        # Resources
        data['coins_fetched'] = parse_number(get_field(r'(?:Coins Fetched|Moedas Obtidas)\s+([\d,.]+[KMBTQSDN]?)', '0'))
        data['gems'] = int(get_field(r'(?:Gems|Joias)\s+(\d+)', '0'))
        data['medals'] = int(get_field(r'(?:Medals|Medalhas)\s+(\d+)', '0'))
        data['reroll_shards'] = int(
            get_field(r'(?:Reroll Shards|Fragmentos de Variação)(?!\s+(?:Earned|Obtidos))\s+([\d,]+)', '0').replace(',',
                                                                                                                    '').replace(
                '.', ''))
        data['cannon_shards'] = int(
            get_field(r'(?:Cannon Shards|Fragmentos de Canhão)\s+([\d,]+)', '0').replace(',', '').replace('.', ''))
        data['armor_shards'] = int(
            get_field(r'(?:Armor Shards|Fragmentos de Armadura)\s+([\d,]+)', '0').replace(',', '').replace('.', ''))
        data['generator_shards'] = int(
            get_field(r'(?:Generator Shards|Fragmentos de Gerador)\s+([\d,]+)', '0').replace(',', '').replace('.', ''))
        data['core_shards'] = int(
            get_field(r'(?:Core Shards|Fragmentos de Núcleo)\s+([\d,]+)', '0').replace(',', '').replace('.', ''))
        data['common_modules'] = int(
            get_field(r'(?:Common Modules|Módulos Comuns)\s+([\d,]+)', '0').replace(',', '').replace('.', ''))
        data['rare_modules'] = int(
            get_field(r'(?:Rare Modules|Módulos Raros)\s+([\d,]+)', '0').replace(',', '').replace('.', ''))

        print(f"✓ Parsed: Tier {data['tier']}, Wave {data['wave']}, Coins {data['coins_earned']}")

        return data

    except Exception as e:
        print(f"✗ Erro no parser: {str(e)}")
        import traceback
        traceback.print_exc()
        return None