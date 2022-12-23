if __name__ == "__main__":

    file = "sample.txt"
    with open(file, "r") as input:
        with open(file.replace(".txt", ".puml"), "w") as output:

            output.write("@startuml\n")
            output.write("!pragma layout smetana\n")
            links = list()

            for line in input:
                line = line.strip()
                line = line.replace("tunnels", "tunnel").replace("valves", "valve").replace("leads", "lead")
                parts = line.split(" has flow rate=")
                valveName = parts[0][len("Valve "):]

                parts = parts[1].split("; tunnel lead to valve ")
                rate = int(parts[0])
                leads = parts[1].split(", ")

                print("Valve %s (%i) -> %s" % (valveName, rate, "/".join(leads)))

                output.write("[%s \\n %i] as %s\n" % (valveName, rate, valveName))
                for lead in leads:
                    links.append((valveName, lead))

            for v1, v2 in links:
                output.write("%s-%s\n" % (v1, v2))

            output.write("@enduml\n")
