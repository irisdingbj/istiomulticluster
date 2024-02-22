# Introduction 

[**Ray Serve**](https://docs.ray.io/en/latest/serve/index.html) is a scalable and framework-agnostic model serving library that allows developers to build online inference APIs with Python. Serve is built on top of Ray, so it easily scales to many machines and offers flexible scheduling support such as fractional GPUs so you can share resources and serve many machine learning models at low cost. Ray Serve can run on any Kubernetes cluster using KubeRay, providing the benefits of both Ray's user experience and scalable compute, and Kubernetes' operational features.

In this project, we will explore how to use **Ray Serve** on **Azure Kubernetes Service (AKS)** to deploy deep learning models. We will start by deploying a simple "Hello World" service on AKS using Ray Serve and the KubeRay operator. Then, we will deploy a Hugging Face model on AKS using Ray Serve and the KubeRay operator. Finally, we will explore how to autoscale the Hugging Face model using Ray Serve and the KubeRay operator.

# About this Repository
This repository contains the Ray deployment code used to deploy models on Ray Serve and AKS. To deploy these services, use the configuration files in the [RayServe_AKS](https://github.com/Rowena2001/RayServe_AKS) repo.
