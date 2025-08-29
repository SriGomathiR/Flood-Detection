import random

class GeneticAlgorithm:
    def __init__(self, population_size, generations, mutation_rate, dataset):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.dataset = dataset  

    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            individual = [
                random.uniform(0, 1),  # temp weight
                random.uniform(0, 1),  # humidity weight
                random.uniform(0, 1),  # rainfall weight
                random.uniform(0, 1)   # soil moisture weight
            ]
            population.append(individual)
        return population

    def fitness(self, individual, weather_data):
        """Evaluate flood risk score using weights * weather features"""
        temp, humidity, rainfall, soil = weather_data
        score = (
            individual[0]*temp +
            individual[1]*humidity +
            individual[2]*rainfall +
            individual[3]*soil
        )
        return score  

    def selection(self, population, scores):
        sorted_pop = [x for _, x in sorted(zip(scores, population), key=lambda pair: pair[0], reverse=True)]
        return sorted_pop[:2]

    def crossover(self, parent1, parent2):
        point = random.randint(1, len(parent1)-1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2

    def mutate(self, individual):
        for i in range(len(individual)):
            if random.random() < self.mutation_rate:
                individual[i] += random.uniform(-0.1, 0.1)
                individual[i] = max(0, min(1, individual[i]))  
        return individual

    def run(self, weather_data):
        population = self.initialize_population()

        for _ in range(self.generations):
            scores = [self.fitness(ind, weather_data) for ind in population]
            parents = self.selection(population, scores)
            next_gen = []

            while len(next_gen) < self.population_size:
                child1, child2 = self.crossover(parents[0], parents[1])
                next_gen.append(self.mutate(child1))
                if len(next_gen) < self.population_size:
                    next_gen.append(self.mutate(child2))

            population = next_gen

        final_scores = [self.fitness(ind, weather_data) for ind in population]
        best_idx = final_scores.index(max(final_scores))
        return population[best_idx], max(final_scores)
