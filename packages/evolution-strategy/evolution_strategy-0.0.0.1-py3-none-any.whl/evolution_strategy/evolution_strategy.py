# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2020 p-cub.cn, Inc. All Rights Reserved
#
###############################################################################
"""
进化策略

Authors: fubo
Date: 2020/03/11 00:00:00
"""
import os
import sys
import logging
import random
import copy
from enum import Enum
from typing import List, Any
from abc import abstractmethod

from pydantic import BaseModel
from tensorboardX import SummaryWriter
import math


class GeneValueType(Enum):
    # FLOAT类型gene数据
    FLOAT = 0

    # INT类型gene数据
    INT = 1


class Gene(BaseModel):
    # Gene数据
    data: List[Any]

    # 变异强度
    strength: List[float]

    # 基因适应度
    fitness: float = 0.0


class ValueRange(BaseModel):
    """ 取值范围 """
    max_value: Any = 1.0

    min_value: Any = 0.0


class ESConfig(BaseModel):
    # tensorboard log path
    tf_log_dir: str = "tf_log"

    # 种群数量
    group_count: int = 9

    # 基因数量（参数个数）
    gene_size: int = 2

    # 基因类型
    gene_value_type: GeneValueType = GeneValueType.FLOAT

    # 变异概率
    mutate_prob: float = 0.05

    # 淘汰比例
    eliminate_ratio: float = 0.2

    # 重整概率
    invade_prob: float = 0.5

    # 参数范围
    value_range: List[ValueRange] = [ValueRange(max_value=1.0, min_value=0.0), ValueRange(max_value=1.0, min_value=0.0)]

    # 最大迭代次数
    max_times: int = 100

    # # 参数最大值
    # max_value: Any = 1.0
    #
    # # 参数最小值
    # min_value: Any = 0.0


class EvolutionStrategy(object):

    def __init__(self, config: ESConfig = ESConfig()):
        """
        初始化进化策略
        :param config: 进化策略配置
        """
        self.config = config
        if config.tf_log_dir != "":
            self.tf_logger = SummaryWriter(config.tf_log_dir)
        else:
            self.tf_logger = None

        if config.gene_size != len(config.value_range):
            raise ValueError

        # CPU内核数量（最大并发的任务数量，使用1/3的cpu资源）
        self.MAX_WORKER = 0
        self.population = []

        # 初始化种群
        self.__init_population()

    def __init_population(self):
        """
        初始化population
        :return:
        """
        for i in range(self.config.group_count):
            data = []
            if self.config.gene_value_type == GeneValueType.FLOAT:
                data = [
                    random.uniform(
                        self.config.value_range[i].min_value, self.config.value_range[i].max_value
                    ) for i in range(self.config.gene_size)
                ]
            if self.config.gene_value_type == GeneValueType.INT:
                data = [
                    int(random.uniform(
                        self.config.value_range[i].min_value, self.config.value_range[i].max_value + 1)
                    ) for i in range(self.config.gene_size)
                ]

            strength = [random.random() for _ in range(self.config.gene_size)]
            self.population.append(Gene(data=data, strength=strength, fitness=0.0))

    def __cross_mutate(self, gene1: Gene, gene2: Gene):
        """
        交叉&变异
        :param gene1:
        :param gene2:
        :return:
        """
        # 查找交叉点
        cross_pos = random.randint(0, self.config.gene_size)

        # 基因交叉
        gene = Gene(
            data=gene1.data[:cross_pos] + gene2.data[cross_pos:],
            strength=gene1.strength[:cross_pos] + gene2.strength[cross_pos:],
            fitness=0.0
        )

        # 基因变异
        if random.random() < self.config.mutate_prob:
            mutate_pos = random.randint(0, self.config.gene_size - 1)
            mutate_change_value = gene.strength[mutate_pos] * random.uniform(-1, 1)
            mutate_strength = random.random()
            logging.info(
                "Mutated original gene=%s, mutate_pos=%s, change_value=%s, change_strength=%s" % (
                    str(gene.data), str(mutate_pos), str(mutate_change_value), str(mutate_strength)
                )
            )
            if self.config.gene_value_type == GeneValueType.INT:
                gene.data[mutate_pos] = int(gene.data[mutate_pos] + mutate_change_value)
            if self.config.gene_value_type == GeneValueType.FLOAT:
                gene.data[mutate_pos] = gene.data[mutate_pos] + mutate_change_value

            if gene.data[mutate_pos] > self.config.value_range[mutate_pos].max_value:
                gene.data[mutate_pos] = self.config.value_range[mutate_pos].max_value

            if gene.data[mutate_pos] < self.config.value_range[mutate_pos].min_value:
                gene.data[mutate_pos] = self.config.value_range[mutate_pos].min_value

            gene.strength[mutate_pos] = mutate_strength
        gene.fitness = 0.0
        return gene

    def __generate(self):
        """
        生成基因
        :return:
        """
        kids_count = self.config.group_count - len(self.population)
        if kids_count == 0:
            return
        kids = []
        for i in range(kids_count):
            f_gene = random.choice(self.population)
            g_gene = random.choice(self.population)
            kid = self.__cross_mutate(f_gene, g_gene)
            kids.append(kid.copy())
        kids = self.__callback_fitness(kids)
        self.population = self.population + kids
        self.population.sort(key=lambda obj: obj.fitness, reverse=True)
        return True

    def __eliminate(self):
        """
        排名靠后的个体被删除，不再参与后续的进化
        :return:
        """
        elim_count = int(len(self.population) * self.config.eliminate_ratio)
        if elim_count == 0:
            elim_count = 1
        self.population = self.population[:-1 * elim_count]
        return True

    def __average_fitness(self):
        """
        平均适应度
        :return:
        """
        return sum([elem.fitness for elem in self.population]) / len(self.population)

    def _show(self, times: int):
        """
        Log 打印
        :param times:
        :return:
        """
        logging.info("The Current times=" + str(times) + " Best Gene= " + str(self.population[0].data))
        logging.debug("The Current times=" + str(times) + " Best Strength= " + str(self.population[0].strength))
        logging.debug("The Current times=" + str(times) + " Best Fitness= " + str(self.population[0].fitness))
        logging.info("The Current times=" + str(times) + " Worst Gene= " + str(self.population[-1].data))
        logging.debug("The Current times=" + str(times) + " Worst Strength= " + str(self.population[-1].strength))
        logging.debug("The Current times=" + str(times) + " Worst Fitness= " + str(self.population[-1].fitness))
        logging.info("The Current times=" + str(times) + " Average Fitness= " + str(self.__average_fitness()))
        fitness_data = [str(elem.fitness) for elem in self.population]
        logging.info("The Current times=" + str(times) + " All Fitness=" + ",".join(fitness_data))

        if self.tf_logger is not None:
            # log fitnessSummary name
            fitness_data_scalar = {
                "best": self.population[0].fitness,
                "worst": self.population[-1].fitness,
                "average": self.__average_fitness()
            }
            self.tf_logger.add_scalars("Fitness/Epoch", fitness_data_scalar, times)

            # log gene

            gene_data_scalar = {}
            for index, gene in enumerate(zip(self.population[0].data, self.population[-1].data)):
                gene_best_key = "best_" + str(index)
                gene_worst_key = "worst_" + str(index)
                gene_best_data = gene[0]
                gene_worst_data = gene[1]
                gene_data_scalar[gene_best_key] = gene_best_data
                gene_data_scalar[gene_worst_key] = gene_worst_data
            self.tf_logger.add_scalars("Gene/Epoch", gene_data_scalar, global_step=times)

    def __invade(self):
        """
        种群重整
        :return:
        """
        # 按照当前最优的gene生成新种群
        sample = self.population[0]
        tmp_population = []
        for i in range(self.config.group_count):
            data = []
            if self.config.gene_value_type == GeneValueType.INT:
                data = [int(random.uniform(-2, 2) + sample.data[j]) for j in range(self.config.gene_size)]
            if self.config.gene_value_type == GeneValueType.FLOAT:
                data = [random.uniform(-2, 2) + sample.data[j] for j in range(self.config.gene_size)]
            for j in range(len(data)):
                if data[j] > self.config.value_range[j].max_value:
                    data[j] = self.config.value_range[j].max_value
                if data[j] < self.config.value_range[j].min_value:
                    data[j] = self.config.value_range[j].min_value
            gene = Gene(
                data=copy.deepcopy(data),
                strength=[random.random() for _ in range(self.config.gene_size)],
                fitness=0.0
            )
            tmp_population.append(gene.copy())
        tmp_population = self.__callback_fitness(tmp_population)
        self.population = self.population + tmp_population

        # 重新生成种群
        self.population.sort(key=lambda obj: obj.fitness, reverse=True)

        # 扔掉劣质个体
        self.population = self.population[:self.config.group_count]

        return True

    def __invade_chance(self) -> bool:
        """
        选择合适的时机进行种群重整
        :return:
        """
        if (self.population[0].fitness - self.population[-1].fitness) > 0.0001:
            # 种群存在差异
            return False

        if random.random() >= self.config.invade_prob:
            # 随机因素
            return False

        return True

    @abstractmethod
    def fitness(self, index: int, weights: List) -> (int, float):
        raise NotImplementedError

    def __callback_fitness(self, genes):
        """
        计算fitness，如果max_worker为0，则使用单进程计算fitness
        :param fitness_fun: 回调函数 输入参数（int, list）,返回(int, float)
        :param genes: gene列表
        :return:
        """
        for index, gene in enumerate(genes):
            idx, genes[index].fitness = self.fitness(index, gene.data)

        return genes

    def start(self, max_generation_count: int = 0):
        """
        :param max_generation_count: 最大迭代次数
        :return:
        """
        # 计算初始种群的fitness
        self.population = self.__callback_fitness(self.population)
        self.population.sort(key=lambda obj: obj.fitness, reverse=True)
        self.config.max_times = max_generation_count if max_generation_count > 0 else self.config.max_times
        # 开始迭代种群
        for i in range(self.config.max_times):
            logging.info("Start Evolution times=" + str(i + 1))
            self.__eliminate()
            self.__generate()
            if self.__invade_chance() is True:
                logging.info("Invade Group times=" + str(i + 1))
                self.__invade()
            self._show(i + 1)
            logging.info("End Evolution times=" + str(i + 1))
        return True

    def get_best_gene(self):
        """
        获取最优的参数
        :return:
        """
        return self.population[0].data


def main():
    class MathSine(EvolutionStrategy):
        def __init__(self, config: ESConfig):
            config.tf_log_dir = "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/log/tf_log"
            super().__init__(config=config)

        def fitness(self, index: int, weights: List) -> (int, float):
            return index, math.sin(weights[0]) * weights[1]

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        stream=sys.stderr
    )

    logging.info("Create ES")
    config = ESConfig()
    config.gene_value_type = GeneValueType.FLOAT
    config.value_range = [ValueRange(max_value=2 * 3.14, min_value=0.0), ValueRange(max_value=1.0, min_value=0.0)]
    config.max_times = 100
    math_sine = MathSine(config=config)

    logging.info("Run Evolution")
    math_sine.start()
    logging.info("Evolution Finish")
    print("The best params is %s" % str(math_sine.get_best_gene()))


if __name__ == '__main__':
    main()
