# Synthetic Dataset Generation for Tomato Ripening Stage Detection

This repository contains the code associated with the paper:
> "Synthetic Dataset Generation for Tomato Ripening Stage Detection 
> in Different Scenes" - IEEE Latin America Transactions

## Description
Pipeline for generating synthetic greenhouse datasets using a 
genetic algorithm, background substitution, and leaf occlusion 
for tomato ripening stage detection based on NMX-FF-031-1997.

## Dataset
The base dataset (3,000 images, 6 ripening stages + masks) 
is available on Kaggle: [https://www.kaggle.com/datasets/gerardoantony/dataset-for-tomatoes-to-use-for-augmentation]

## Requirements
pip install -r requirements.txt

## Usage
python argumentation1_1.py --weights weights.pt --data tomates.ymal --epochs 100 

## Citation
If you use this code, please cite our paper:
[Agregar referencia IEEE cuando esté publicado]
