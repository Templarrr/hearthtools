import json
import random
from perfect_curve_monte_carlo import ManaCurve, ImitateGame

cached_file = 'mana_curves_json'
try:
    with open(cached_file, 'r') as f:
        mc_results_cache = json.load(f)
        best_mana_unspent = min(mc_results_cache.values())
        best_mc = mc_results_cache.keys()[mc_results_cache.values().index(best_mana_unspent)]
except Exception as e:
    best_mana_unspent = 200
    best_mc = '-'
    mc_results_cache = {
        best_mc:best_mana_unspent
    }

print 'best cached curve %s %f' % (best_mc, best_mana_unspent)
print 'mana curves processed %d' % len(mc_results_cache)

for i in range(1000):
    mc = ManaCurve()
    while not mc.is_unusable():
        if str(mc) in mc_results_cache:
            mc.push_mana_curve()
            continue
        mc_results = []
        for i in range(1000):
            ig = ImitateGame(mc.get_deck(), 12)
            mc_results.append(ig.imitate_game())
        avg_mana_unspent = sum(mc_results)/float(len(mc_results))
        if avg_mana_unspent<best_mana_unspent:
            best_mana_unspent = avg_mana_unspent
            best_mc = str(mc)
            print 'Average mana lost for %s is %f' % (best_mc, best_mana_unspent)
        mc_results_cache[str(mc)] = avg_mana_unspent
        if random.randint(1,10):
            with open(cached_file, 'w') as f:
                json.dump(mc_results_cache, f)
        mc.push_mana_curve()
# With hero power
# 0:0:0:9:7:3:2:4:5:0:0 is 1.511200 - Shaman or Paladin deck? Something that can use double hp in the start

# More realistic variants
# Average mana lost for 0:1:2:4:8:5:2:3:3:1:1 is 1.795500
# Average mana lost for 0:1:2:2:9:6:2:2:4:1:1 is 1.746900
# Average mana lost for 0:1:2:2:8:7:2:2:4:1:1 is 1.743600

# Without hero power
# Average mana lost for 0:1:1:5:4:8:4:4:0:2:1 is 6.930100
# Average mana lost for 0:1:1:4:8:4:4:4:2:0:2 is 6.683000
# Average mana lost for 0:0:0:3:5:7:4:4:2:2:3 is 6.632000

# Average mana lost for 0:0:3:5:5:6:4:2:3:1:1 is 6.547000
# Average mana lost for 0:0:3:5:5:5:4:3:3:0:2 is 6.426000
# Average mana lost for 0:0:1:6:5:5:5:3:3:0:2 is 6.343000
# Average mana lost for 0:0:2:4:6:7:4:3:1:1:2 is 6.280000
# Average mana lost for 0:0:1:5:6:6:5:3:1:1:2 is 6.128000
# Average mana lost for 0:0:1:5:5:6:3:3:2:2:3 is 6.047000
# Average mana lost for 0:0:0:6:4:7:3:3:2:2:3 is 6.045000
# Average mana lost for 0:0:3:5:5:7:2:3:1:2:2 is 5.989000
# Average mana lost for 0:0:2:5:7:5:2:3:1:2:3 is 5.952000
# Average mana lost for 0:0:2:6:5:3:5:2:2:1:4 is 5.930000
# Average mana lost for 0:0:0:8:5:3:4:2:2:1:5 is 5.898000
# Average mana lost for 0:0:0:7:5:4:3:3:2:1:5 is 5.854000

# With double penalty on skipped turns
# Average mana lost for 0:1:2:5:7:5:4:2:2:2:0 is 9.989000
# Average mana lost for 0:1:2:5:7:4:4:3:2:2:0 is 9.871000
# Average mana lost for 0:1:2:6:7:6:3:2:1:1:1 is 9.868000
# Average mana lost for 0:1:2:6:7:5:4:2:1:1:1 is 9.680000
# Average mana lost for 0:0:3:5:8:5:4:2:1:1:1 is 9.541000
# Average mana lost for 0:0:2:6:9:3:4:1:2:2:1 is 9.536000
# Average mana lost for 0:0:2:6:9:3:4:1:2:1:2 is 9.147000
# Average mana lost for 0:0:1:9:4:5:5:1:2:1:2 is 9.001000
# Average mana lost for 0:0:5:6:4:4:2:3:3:1:2 is 8.754000
# Average mana lost for 0:0:5:6:4:4:2:3:2:2:2 is 8.697000