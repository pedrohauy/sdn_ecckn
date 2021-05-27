from .sensors import Sensor
from tqdm import tqdm
import csv
from .shannon_entropy import sample_entropy

def run(rounds, neighbors=3):
    # Sensors initialization

    a = Sensor("A", True, "-", (20,9))
    b = Sensor("B", True, 2.67944, (39,6))
    c = Sensor("C", True, 2.72095, (39,3))
    d = Sensor("D", True, 2.69165, (33,6))
    e = Sensor("E", True, 2.73315, (31,3))
    f = Sensor("F", True, 2.72827, (31,6))
    g = Sensor("G", True, 2.72827, (31,9))
    h = Sensor("H", True, 2.73804, (31,12))
    i = Sensor("I", True, 2.66479, (41,9))
    j = Sensor("J", True, 2.69409, (41,12))

    network = [b, c, d, e, f, g, h, i, j]
    core = [d, e, f, g, h]

    # Dictionaries to store sensor status and energies

    status = {
        "B": [],  "C": [], "D": [], "E": [], "F": [], "G": [], "H": [], "I": [], "J": []
    }

    energies = {
        "B": [],  "C": [], "D": [], "E": [], "F": [], "G": [], "H": [], "I": [], "J": []
    }

    for node in network:
        status[node.name].append(node.awake)
        energies[node.name].append(node.energy)

    # Load requests from csv file

    broker_requests = []

    with open('./simulations/traffic/dos_attack.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file,delimiter=';')
        line_count = 0
        for line in csv_reader:
            if line_count != 0:
                # remove timestamps
                request = list(line.values())[1:]
                broker_requests.append(request)
            line_count += 1

    # Estimate Shannon Entropy

    entropy = sample_entropy('./simulations/traffic/dos_attack.csv', 200)

    # Start simulation

    for step in tqdm(range(rounds), desc="SDN-ECCKN with Anti-Dos"):
        if step >= 200:
            if entropy <= 0.91289635348511:
                broker_requests[step][2] = 'X'

        for node in network:
            if node.name in broker_requests[step]:
                node.awake = True
            else:
                node.awake = True if node.energy >= Sensor.highest_energy(network, k=neighbors) else False

        if (not d.awake) and (not e.awake) and (not f.awake) and (not g.awake) and (not h.awake):
            for inner_node in core:
                inner_node.awake = True if inner_node.energy >= Sensor.highest_energy(core, k=1) else False

        # Sensor b energy calculation
        if b.awake:
            if d.awake:
                b.transmit_to(d)
            else:
                if e.awake:
                    b.transmit_to(e)
                else:
                    if f.awake:
                        b.transmit_to(f)
                    else:
                        if g.awake:
                            b.transmit_to(g)
                        else:
                            if h.awake:
                                b.transmit_to(h)
        else:
            b.sleep

        # Sensor c energy calculation
        if c.awake:
            if d.awake:
                c.transmit_to(d)
            else:
                if e.awake:
                    c.transmit_to(e)
                else:
                    if f.awake:
                        c.transmit_to(f)
                    else:
                        if g.awake:
                            c.transmit_to(g)
                        else:
                            if h.awake:
                                c.transmit_to(h)
        else:
            c.sleep

        # Sensor d energy calculation
        if d.awake:
            d.transmit_to(a)
        else:
            d.sleep

        # Sensor e energy calculation
        if e.awake:
            e.transmit_to(a)
        else:
            e.sleep

        # Sensor f energy calculation
        if f.awake:
            f.transmit_to(a)
        else:
            f.sleep

        # Sensor g energy calculation
        if g.awake:
            g.transmit_to(a)
        else:
            g.sleep

        # Sensor h energy calculation
        if h.awake:
            h.transmit_to(a)
        else:
            h.sleep

        # Sensor i energy calculation
        if i.awake:
            if d.awake:
                i.transmit_to(d)
            else:
                if e.awake:
                    i.transmit_to(e)
                else:
                    if f.awake:
                        i.transmit_to(f)
                    else:
                        if g.awake:
                            i.transmit_to(g)
                        else:
                            if h.awake:
                                i.transmit_to(h)
        else:
            i.sleep

        # Sensor j energy calculation
        if j.awake:
            if d.awake:
                j.transmit_to(d)
            else:
                if e.awake:
                    j.transmit_to(e)
                else:
                    if f.awake:
                        j.transmit_to(f)
                    else:
                        if g.awake:
                            j.transmit_to(g)
                        else:
                            if h.awake:
                                j.transmit_to(h)
        else:
            j.sleep

        # Record simulations

        for node in network:
            status[node.name].append(node.awake)
            energies[node.name].append(node.energy)

    return status, energies
