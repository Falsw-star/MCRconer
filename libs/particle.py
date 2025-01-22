from libs import libuffer


class Particle (object):
	TYPE = -1
	NAME = "?"
	
	def read_buf(self, buf):
		pass
	
	def write_buf(self, buf):
		pass


class AmbientEntityEffect (Particle):
	TYPE = 0
	NAME = 'minecraft:ambient_entity_effect'


class AngryVillager (Particle):
	TYPE = 1
	NAME = 'minecraft:angry_villager'
	

class Block (Particle):
	TYPE = 2
	NAME = 'minecraft:block'
	
	def __init__(self, block_state = 0):
		self.block_state = block_state
		
	def read_buf(self, buf):
		self.block_state = buf.read_varint()
	
	def write_buf(self, buf):
		buf.write_varint(self.block_state)


class BlockMarker (Particle):
	TYPE = 3
	NAME = 'minecraft:block_marker'
	
	def __init__(self, block_state = 0):
		self.block_state = block_state
		
	def read_buf(self, buf):
		self.block_state = buf.read_varint()
	
	def write_buf(self, buf):
		buf.write_varint(self.block_state)


class Bubble (Particle):
	TYPE = 4
	NAME = 'minecraft:bubble'
	
	
class Cloud (Particle):
	TYPE = 5
	NAME = 'minecraft:cloud'


class Crit (Particle):
	TYPE = 6
	NAME = 'minecraft:crit'


class DamageIndicator (Particle):
	TYPE = 7
	NAME = 'minecraft:damage_indicator'


class DragonBreath (Particle):
	TYPE = 8
	NAME = 'minecraft:dragon_breath'


class DrippingLava (Particle):
	TYPE = 9
	NAME = 'minecraft:dripping_lava'


class FallingLava (Particle):
	TYPE = 10
	NAME = 'minecraft:falling_lava'
	

class LandingLava (Particle):
	TYPE = 11
	NAME = 'minecraft:landing_lava'


class DrippingWater (Particle):
	TYPE = 12
	NAME = 'minecraft:dripping_water'


class FallingWater (Particle):
	TYPE = 13
	NAME = 'minecraft:falling_water'


class Dust (Particle):
	TYPE = 14
	NAME = 'minecraft:dust'
	
	def __init__(self, rgb=[0,0,0], scale=0.0):
		self.rgb = rgb
		self.scale = scale
	
	def read_buf(self, buf):
		self.rgb = [buf.read_float() for _ in range(3)]
		self.scale = buf.read_float()
	
	def write_buf(self, buf):
		for i in range(3):
			buf.write_float(self.rgb[i])
		buf.write_float(self.scale)


class DustColorTransition (Particle):
	TYPE = 15
	NAME = 'minecraft:dust_color_transition'
	
	def __init__(self, orig=[0,0,0], scale=0.0, to=[0,0,0]):
		self.orig = orig
		self.scale = scale
		self.to = to
	
	def read_buf(self, buf):
		self.orig = [buf.read_float() for _ in range(3)]
		self.scale = buf.read_float()
		self.to = [buf.read_float() for _ in range(3)]
	
	def write_buf(self, buf):
		for i in range(3):
			buf.write_float(self.orig[i])
		buf.write_float(self.scale)
		for i in range(3):
			buf.write_float(self.to[i])


class Effect (Particle):
	TYPE = 16
	NAME = 'minecraft:effect'


class ElderGuardian (Particle):
	TYPE = 17
	NAME = 'minecraft:elder_guardian'


class EnchantedHit (Particle):
	TYPE = 18
	NAME = 'minecraft:enchanted_hit'


class Enchant (Particle):
	TYPE = 19
	NAME = 'minecraft:enchant'


class EndRod (Particle):
	TYPE = 20
	NAME = 'minecraft:end_rod'


class EntityEffect (Particle):
	TYPE = 21
	NAME = 'minecraft:entity_effect'


class ExplosionEmitter (Particle):
	TYPE = 22
	NAME = 'minecraft:explosion_emitter'


class Explosion (Particle):
	TYPE = 23
	NAME = 'minecraft:explosion'


class SonicBoom (Particle):
	TYPE = 24
	NAME = 'minecraft:sonic_boom'
	
	
class FallingDust (Particle):
	TYPE = 25
	NAME = 'minecraft:falling_dust'
	
	def __init__(self, block_state = 0):
		self.block_state = block_state
		
	def read_buf(self, buf):
		self.block_state = buf.read_varint()
	
	def write_buf(self, buf):
		buf.write_varint(self.block_state)


class Firework (Particle):
	TYPE = 26
	NAME = 'minecraft:firework'
	

class Fishing (Particle):
	TYPE = 27
	NAME = 'minecraft:fishing'


class Flame (Particle):
	TYPE = 28
	NAME = 'minecraft:flame'


class CherryLeaves (Particle):
	TYPE = 29
	NAME = 'minecraft:cherry_leaves'


class SculkSoul (Particle):
	TYPE = 30
	NAME = 'minecraft:sculk_soul'


class SculkCharge (Particle):
	TYPE = 31
	NAME = 'minecraft:sculk_charge'
	
	def __init__(self, roll = 0.0):
		self.roll = roll
	
	def read_buf(self, buf):
		self.roll = buf.read_float()
	
	def write_buf(self, buf):
		buf.write_float(self.roll)


class SculkChargePop (Particle):
	TYPE = 32
	NAME = 'minecraft:sculk_charge_pop'


class SoulFireFlame (Particle):
	TYPE = 33
	NAME = 'minecraft:soul_fire_flame'


class Soul (Particle):
	TYPE = 34
	NAME = 'minecraft:soul'


class Flash (Particle):
	TYPE = 35
	NAME = 'minecraft:flash'


class HappyVillager (Particle):
	TYPE = 36
	NAME = 'minecraft:happy_villager'


class Composter (Particle):
	TYPE = 37
	NAME = 'minecraft:composter'


class Heart (Particle):
	TYPE = 38
	NAME = 'minecraft:heart'
	

class InstantEffect (Particle):
	TYPE = 39
	NAME = 'minecraft:instant_effect'
	

"""
class Item (Particle):
	TYPE = 40
	NAME = 'minecraft:item'
	
	def __init__(self, slot=sl.Slot()):
		self.slot = slot
	
	def read_buf(self, buf):
		self.slot = sl.Slot.read_buffer(buf)
	
	def write_buf(self, buf):
		self.slot.write_buffer(buf)
"""


class Vibration (Particle):
	TYPE = 41
	NAME = 'minecraft:vibration'
	
	def __init__(self, position_source_type='', block_position=[0,0,0], entity_id=0, entity_eye_height=0.0, ticks=0):
		self.position_source_type = position_source_type
		self.block_position = block_position
		self.entity_id = entity_id
		self.entity_eye_height = entity_eye_height
		self.ticks = ticks
	
	def read_buf(self, buf):
		self.position_source_type = buf.read_str()
		self.block_position = buf.read_position()
		self.entity_id = buf.read_varint()
		self.entity_eye_height = buf.read_float()
		self.ticks = buf.read_varint()
	
	def write_buf(self, buf):
		buf.write_str(self.position_source_type)
		buf.write_position(self.block_position)
		buf.write_varint(self.entity_id)
		buf.write_float(self.entity_eye_height)
		buf.write_varint(self.ticks)
	

class ItemSlime (Particle):
	TYPE = 42
	NAME = 'minecraft:item_slime'


class ItemSnowball (Particle):
	TYPE = 43
	NAME = 'minecraft:item_snowball'


class LargeSmoke (Particle):
	TYPE = 44
	NAME = 'minecraft:large_smoke'


class Lava (Particle):
	TYPE = 45
	NAME = 'minecraft:lava'


class Mycelium (Particle):
	TYPE = 46
	NAME = 'minecraft:mycelium'


class Note (Particle):
	TYPE = 47
	NAME = 'minecraft:note'



class Poof (Particle):
	TYPE = 48
	NAME = 'minecraft:poof'



class Portal (Particle):
	TYPE = 49
	NAME = 'minecraft:portal'



class Rain (Particle):
	TYPE = 50
	NAME = 'minecraft:rain'



class Smoke (Particle):
	TYPE = 51
	NAME = 'minecraft:smoke'



class Sneeze (Particle):
	TYPE = 52
	NAME = 'minecraft:sneeze'



class Spit (Particle):
	TYPE = 53
	NAME = 'minecraft:spit'



class SquidInk (Particle):
	TYPE = 54
	NAME = 'minecraft:squid_ink'



class SweepAttack (Particle):
	TYPE = 55
	NAME = 'minecraft:sweep_attack'



class TotemOfUndying (Particle):
	TYPE = 56
	NAME = 'minecraft:totem_of_undying'



class Underwater (Particle):
	TYPE = 57
	NAME = 'minecraft:underwater'



class Splash (Particle):
	TYPE = 58
	NAME = 'minecraft:splash'



class Witch (Particle):
	TYPE = 59
	NAME = 'minecraft:witch'



class BubblePop (Particle):
	TYPE = 60
	NAME = 'minecraft:bubble_pop'



class CurrentDown (Particle):
	TYPE = 61
	NAME = 'minecraft:current_down'



class BubbleColumnUp (Particle):
	TYPE = 62
	NAME = 'minecraft:bubble_column_up'



class Nautilus (Particle):
	TYPE = 63
	NAME = 'minecraft:nautilus'



class Dolphin (Particle):
	TYPE = 64
	NAME = 'minecraft:dolphin'



class CampfireCosySmoke (Particle):
	TYPE = 65
	NAME = 'minecraft:campfire_cosy_smoke'



class CampfireSignalSmoke (Particle):
	TYPE = 66
	NAME = 'minecraft:campfire_signal_smoke'



class DrippingHoney (Particle):
	TYPE = 67
	NAME = 'minecraft:dripping_honey'



class FallingHoney (Particle):
	TYPE = 68
	NAME = 'minecraft:falling_honey'



class LandingHoney (Particle):
	TYPE = 69
	NAME = 'minecraft:landing_honey'



class FallingNectar (Particle):
	TYPE = 70
	NAME = 'minecraft:falling_nectar'



class FallingSporeBlossom (Particle):
	TYPE = 71
	NAME = 'minecraft:falling_spore_blossom'



class Ash (Particle):
	TYPE = 72
	NAME = 'minecraft:ash'



class CrimsonSpore (Particle):
	TYPE = 73
	NAME = 'minecraft:crimson_spore'



class WarpedSpore (Particle):
	TYPE = 74
	NAME = 'minecraft:warped_spore'



class SporeBlossomAir (Particle):
	TYPE = 75
	NAME = 'minecraft:spore_blossom_air'



class DrippingObsidianTear (Particle):
	TYPE = 76
	NAME = 'minecraft:dripping_obsidian_tear'



class FallingObsidianTear (Particle):
	TYPE = 77
	NAME = 'minecraft:falling_obsidian_tear'



class LandingObsidianTear (Particle):
	TYPE = 78
	NAME = 'minecraft:landing_obsidian_tear'



class ReversePortal (Particle):
	TYPE = 79
	NAME = 'minecraft:reverse_portal'



class WhiteAsh (Particle):
	TYPE = 80
	NAME = 'minecraft:white_ash'



class SmallFlame (Particle):
	TYPE = 81
	NAME = 'minecraft:small_flame'



class Snowflake (Particle):
	TYPE = 82
	NAME = 'minecraft:snowflake'



class DrippingDripstoneLava (Particle):
	TYPE = 83
	NAME = 'minecraft:dripping_dripstone_lava'



class FallingDripstoneLava (Particle):
	TYPE = 84
	NAME = 'minecraft:falling_dripstone_lava'



class DrippingDripstoneWater (Particle):
	TYPE = 85
	NAME = 'minecraft:dripping_dripstone_water'



class FallingDripstoneWater (Particle):
	TYPE = 86
	NAME = 'minecraft:falling_dripstone_water'



class GlowSquidInk (Particle):
	TYPE = 87
	NAME = 'minecraft:glow_squid_ink'



class Glow (Particle):
	TYPE = 88
	NAME = 'minecraft:glow'



class WaxOn (Particle):
	TYPE = 89
	NAME = 'minecraft:wax_on'



class WaxOff (Particle):
	TYPE = 90
	NAME = 'minecraft:wax_off'



class ElectricSpark (Particle):
	TYPE = 91
	NAME = 'minecraft:electric_spark'



class Scrape (Particle):
	TYPE = 92
	NAME = 'minecraft:scrape'

class Shriek (Particle):
	TYPE = 93
	NAME = 'minecraft:shriek'
	
	def __init__(self, delay=0):
		self.delay = delay
	
	def read_buf(self, buf):
		self.delay = buf.read_varint()
	
	def write_buf(self, buf):
		buf.write_varint(self.delay)


class EggCrack (Particle):
	TYPE = 94
	NAME = 'minecraft:egg_crack'


PARTICLES = (AmbientEntityEffect, AngryVillager, Block, BlockMarker, Bubble, Cloud, Crit, DamageIndicator,
			 DragonBreath, DrippingLava, FallingLava, LandingLava, DrippingWater, FallingWater, Dust,
			 DustColorTransition, Effect, ElderGuardian, EnchantedHit, Enchant, EndRod, EntityEffect,
			 ExplosionEmitter, Explosion, SonicBoom, FallingDust, Firework, Fishing, Flame, CherryLeaves,
			 SculkSoul, SculkCharge, SculkChargePop, SoulFireFlame, Soul, Flash, HappyVillager,
			 Composter, Heart, InstantEffect, Vibration, ItemSlime, ItemSnowball, LargeSmoke, Lava,
			 Mycelium, Note, Poof, Portal, Rain, Smoke, Sneeze, Spit, SquidInk, SweepAttack, TotemOfUndying,
			 Underwater, Splash, Witch, BubblePop, CurrentDown, BubbleColumnUp, Nautilus, Dolphin,
			 CampfireCosySmoke, CampfireSignalSmoke, DrippingHoney, FallingHoney, LandingHoney, FallingNectar,
			 FallingSporeBlossom, Ash, CrimsonSpore, WarpedSpore, SporeBlossomAir, DrippingObsidianTear,
			 FallingObsidianTear, LandingObsidianTear, ReversePortal, WhiteAsh, SmallFlame, Snowflake,
			 DrippingDripstoneLava, FallingDripstoneLava, DrippingDripstoneWater, FallingDripstoneWater,
			 GlowSquidInk, Glow, WaxOn, WaxOff, ElectricSpark, Scrape, Shriek, EggCrack)
