from sqlalchemy import Column, String, Integer, Numeric, DateTime
from .database import Base
from datetime import datetime
import uuid
class BattleReport(Base):
    __tablename__ = 'battle_reports'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(16), nullable=False, index=True)

    # Informações básicas
    battle_date = Column(DateTime, nullable=False)
    game_time = Column(String(50))
    real_time = Column(String(50))
    tier = Column(Integer)
    wave = Column(Integer)
    killed_by = Column(String(100))

    # Valores grandes
    coins_earned = Column(Numeric(50, 2))
    coins_per_hour = Column(Numeric(50, 2))
    cash_earned = Column(Numeric(50, 2))
    interest_earned = Column(Numeric(50, 2))
    gem_blocks_tapped = Column(Integer)
    cells_earned = Column(Numeric(50, 2))
    reroll_shards_earned = Column(Numeric(50, 2))

    # Danos
    damage_dealt = Column(Numeric(50, 2))
    damage_taken = Column(Numeric(50, 2))
    damage_taken_wall = Column(Numeric(50, 2))
    damage_taken_while_berserked = Column(Numeric(50, 2))
    damage_gain_from_berserk = Column(Numeric(50, 2))

    # Stats gerais
    death_defy = Column(Integer)
    lifesteal = Column(Numeric(50, 2))

    # Danos por tipo
    projectiles_damage = Column(Numeric(50, 2))
    projectiles_count = Column(Numeric(50, 2))
    thorn_damage = Column(Numeric(50, 2))
    orb_damage = Column(Numeric(50, 2))
    enemies_hit_by_orbs = Column(Numeric(50, 2))
    land_mine_damage = Column(Numeric(50, 2))
    land_mines_spawned = Column(Integer)
    rend_armor_damage = Column(Numeric(50, 2))
    death_ray_damage = Column(Numeric(50, 2))
    smart_missile_damage = Column(Numeric(50, 2))
    inner_land_mine_damage = Column(Numeric(50, 2))
    chain_lightning_damage = Column(Numeric(50, 2))
    death_wave_damage = Column(Numeric(50, 2))
    tagged_by_deathwave = Column(Integer)
    swamp_damage = Column(Numeric(50, 2))
    black_hole_damage = Column(Numeric(50, 2))
    electrons_damage = Column(Numeric(50, 2))

    # Ondas e upgrades
    waves_skipped = Column(Integer)
    recovery_packages = Column(Integer)
    free_attack_upgrade = Column(Integer)
    free_defense_upgrade = Column(Integer)
    free_utility_upgrade = Column(Integer)

    # Recursos de Death Wave
    hp_from_death_wave = Column(Numeric(50, 2))
    coins_from_death_wave = Column(Numeric(50, 2))

    # Recursos de torres especiais
    cash_from_golden_tower = Column(Numeric(50, 2))
    coins_from_golden_tower = Column(Numeric(50, 2))
    coins_from_black_hole = Column(Numeric(50, 2))
    coins_from_spotlight = Column(Numeric(50, 2))
    coins_from_orb = Column(Numeric(50, 2))
    coins_from_coin_upgrade = Column(Numeric(50, 2))
    coins_from_coin_bonuses = Column(Numeric(50, 2))

    # Inimigos
    total_enemies = Column(Integer)
    basic_enemies = Column(Integer)
    fast_enemies = Column(Integer)
    tank_enemies = Column(Integer)
    ranged_enemies = Column(Integer)
    boss_enemies = Column(Integer)
    protector_enemies = Column(Integer)
    total_elites = Column(Integer)
    vampires = Column(Integer)
    rays = Column(Integer)
    scatters = Column(Integer)
    saboteur = Column(Integer)
    commander = Column(Integer)
    overcharge = Column(Integer)

    # Inimigos destruídos por método
    destroyed_by_orbs = Column(Integer)
    destroyed_by_thorns = Column(Integer)
    destroyed_by_death_ray = Column(Integer)
    destroyed_by_land_mine = Column(Integer)
    destroyed_in_spotlight = Column(Integer)

    # Bots
    flame_bot_damage = Column(Numeric(50, 2))
    thunder_bot_stuns = Column(Integer)
    golden_bot_coins_earned = Column(Numeric(50, 2))
    destroyed_in_golden_bot = Column(Integer)

    # Guardian
    guardian_damage = Column(Numeric(50, 2))
    summoned_enemies = Column(Numeric(50, 2))
    guardian_coins_stolen = Column(Numeric(50, 2))

    # Recursos coletados
    coins_fetched = Column(Numeric(50, 2))
    gems = Column(Integer)
    medals = Column(Integer)
    reroll_shards = Column(Integer)
    cannon_shards = Column(Integer)
    armor_shards = Column(Integer)
    generator_shards = Column(Integer)
    core_shards = Column(Integer)
    common_modules = Column(Integer)
    rare_modules = Column(Integer)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'battle_date': self.battle_date.isoformat() if self.battle_date else None,
            'real_time': self.real_time,
            'tier': self.tier,
            'wave': self.wave,
            'coins_earned': float(self.coins_earned) if self.coins_earned else 0,
            'cells_earned': float(self.cells_earned) if self.cells_earned else 0,
            'reroll_shards_earned': float(self.reroll_shards_earned) if self.reroll_shards_earned else 0,
            'damage_dealt': float(self.damage_dealt) if self.damage_dealt else 0,
            'killed_by': self.killed_by,
        }