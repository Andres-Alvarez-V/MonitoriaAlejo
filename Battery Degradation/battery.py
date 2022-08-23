class Battery:
    def __init__(self, size, price=10000):
        self.size = size        # Tamaño
        self.price = price      # Precio
        self.mu = 1             # eficiencia de carga/descarga
        self.a = 694
        self.b = 0.795
        self.ws = price * self.b / (2 * size * (self.mu**2) * self.a)

        self.m = 5963
        self.n = -0.6531
        self.o = 321.4
        self.p = 0.03168

    def acc(self, dod):
        acc_calc = self.a / (dod**self.b)
        return acc_calc

    def awc(self, acc, dod):
        av_wear_cost = self.price / (acc * dod[0] * self.size * (self.mu**2) * 2)
        return av_wear_cost

    def wear_dens(self, dod):
        wear_density = self.ws * (dod**-0.205)
        return wear_density

    def ccost(self, cref, c):
        import math
        ccountref = (self.m * math.exp(self.n * cref)) + (self.o * math.exp(self.p * cref))
        ccount = (self.m * math.exp(self.n * c)) + (self.o * math.exp(self.p * c))
        penalty = ccount/ccountref
        return penalty

    def acc_plot(self, delta, plot=False):
        from matplotlib import pyplot as plt
        import numpy as np
        dod = np.arange(1/delta, 1+1/delta, 1/delta)
        ac_count = np.array([self.acc(i) for i in dod])
        if plot:
            plt.title("ACC / DoD")
            plt.xlabel("Depth of Discharge (%)")
            plt.ylabel("Achievable Cycle Count")
            plt.plot(dod, ac_count)
            plt.show()
        return ac_count, dod

    def awc_plot(self, delta, plot=False):
        from matplotlib import pyplot as plt
        import numpy as np
        ac_count, dod = self.acc_plot(delta)
        awc = self.awc(ac_count, dod)
        awc_delta = np.insert(np.diff(awc), 0, awc[0])
        density = self.wear_dens(dod)
        soc = 1-dod
        if plot:
            plt.title("Wear cost / SoC")
            plt.xlabel("State of Charge (%)")
            plt.ylabel("Wear cost")
            plt.plot(soc, awc_delta)
            plt.plot(soc, density)
            plt.legend(["AWC", "W(s)"])
            plt.show()
        return awc_delta, soc

    def awc_penalty_plot(self, delta, cref, c, plot=False):
        from matplotlib import pyplot as plt
        awc_delta, soc = self.awc_plot(delta)
        penalty = self.ccost(cref, c)
        awc_delta_penalty = awc_delta/penalty
        if plot:
            plt.title("Wear cost / SoC")
            plt.xlabel("State of Charge (%)")
            plt.ylabel("Wear cost")
            plt.plot(soc, awc_delta)
            plt.plot(soc, awc_delta_penalty)
            plt.legend([f"AWC_ref {cref}C", f"AWC_penalty {c}C"])
            plt.show()
        return awc_delta_penalty, soc




