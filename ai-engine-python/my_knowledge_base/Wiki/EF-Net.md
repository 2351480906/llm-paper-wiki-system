## 📋 元数据 (Metadata)
- **文献题目**：EF-Net: Mental State Recognition by Analyzing Multimodal EEG-fNIRS via CNN
- **文献作者**：Aniqa Arif, Yihe Wang, Rui Yin, Xiang Zhang, Ahmed Helmy
- **发表时间**：2024年3月15日
- **发表地址/期刊会议**：*Sensors* 2024, 24, 1889 (MDPI)
- **开源代码地址**：未提及

## 📖 论文摘要 (Abstract 中文翻译)
脑信号分析对于研究心理状态和各种神经系统疾病至关重要。测量脑活动的两种最常用的非侵入性信号是脑电图（EEG）和功能近红外光谱（fNIRS）。EEG具有较高的采样频率，能够捕获更多的时间特征；而fNIRS拥有更多的通道，能够提供更丰富的空间信息。尽管先前的一些研究已经探索了使用多模态深度学习模型来分析EEG和fNIRS的脑活动，但受试者独立（subject-independent）的训练-测试划分分析仍未得到充分探索。受试者独立设置的结果直接展示了模型对未见受试者的处理能力，这对于实际应用至关重要。在本文中，我们介绍了EF-Net，一种基于CNN的新型多模态深度学习模型。我们在一个EEG-fNIRS词语生成（WG）数据集上评估了EF-Net在心理状态识别任务上的表现，主要关注受试者独立设置。为了完整性，我们也报告了受试者依赖（subject-dependent）和受试者半依赖（subject-semidependent）设置下的结果。我们将我们的模型与五种基线方法进行了比较，包括三种传统机器学习方法和两种深度学习方法。EF-Net在准确率和F1分数上均表现出优越的性能，超越了这些基线。我们的模型在受试者依赖、受试者半依赖和受试者独立设置下的F1分数分别达到了99.36%、98.31%和65.05%，分别比最佳基线F1分数高出1.83%、4.34%和2.13%。这些结果凸显了EF-Net能够有效学习和解释不同及未见受试者的心理状态和脑活动的能力。

## 🔍 特征提取项

### 算法结构
基于提供的文本片段，EF-Net 是一种**基于卷积神经网络（CNN）的多模态深度学习模型**。该架构旨在端到端地联合处理 EEG 和 fNIRS 信号，利用深度学习自动提取特征，替代传统机器学习依赖繁琐手工特征提取的流程。模型设计充分利用了两种模态的互补性：EEG 提供高时间分辨率/低空间分辨率的电信号动态变化，fNIRS 提供高空间分辨率/低时间分辨率的血氧代谢信息。通过 CNN 的卷积操作，模型能够并行或融合提取脑活动的时空特征。*(注：由于提供的正文仅包含引言开头部分，网络具体的层数、卷积核大小、融合机制及数学公式未在给定片段中展开。)*

### 训练数据集
论文使用了一个**EEG-fNIRS 词语生成（Word Generation, WG）数据集**。该数据集包含同步采集的脑电与近红外光谱信号，用于心理状态识别任务。实验采用了三种数据划分策略以全面评估模型：
- **受试者依赖（Subject-dependent）**：训练集与测试集包含相同受试者的数据。
- **受试者半依赖（Subject-semidependent）**：部分受试者数据跨训练/测试集划分。
- **受试者独立（Subject-independent）**：训练集与测试集的受试者完全互斥，用于评估模型对未见个体的泛化能力。

### 训练结果表现
EF-Net 在心理状态识别任务上全面优于五种基线方法（3种传统机器学习方法 + 2种深度学习方法），在准确率与 F1 分数上均取得最佳表现。核心指标如下：
- **受试者依赖设置**：F1 分数为 $99.36\%$（较最佳基线提升 $1.83\%$）
- **受试者半依赖设置**：F1 分数为 $98.31\%$（较最佳基线提升 $4.34\%$）
- **受试者独立设置**：F1 分数为 $65.05\%$（较最佳基线提升 $2.13\%$）
结果表明该模型不仅能高效拟合个体特异性脑活动模式，在跨受试者泛化任务中也展现出目前同类方法中的领先性能。

### 创新点
1. **聚焦受试者独立泛化评估**：突破以往脑信号研究多局限于受试者依赖/半依赖设置的局限，将评估重点放在受试者独立划分上，直接验证模型在真实世界中面对全新个体时的可用性。
2. **免手工特征的多模态CNN融合**：提出 EF-Net 架构，无需依赖领域专家进行复杂的信号预处理与手工特征工程，即可实现 EEG 与 fNIRS 的深层特征联合学习。
3. **时空分辨率互补建模**：针对 EEG（高时间/低空间）与 fNIRS（高空间/低时间）的固有物理特性差异，设计网络结构以自动对齐并融合两者的时空维度信息，提升心理状态解码的鲁棒性。

### 局限性
*(基于当前提供的引言片段推断)*
尽管 EF-Net 在受试者独立设置下超越了基线模型，但其 F1 分数（$65.05\%$）仍显著低于受试者依赖设置（$99.36\%$），这揭示了**跨受试者个体差异**（如颅骨厚度、脑区结构差异、基线神经活动漂移等）仍是制约多模态脑信号模型泛化性能的核心瓶颈。此外，受限于提供的文本长度，论文关于计算复杂度、实时推理延迟、硬件部署成本以及特定噪声环境下的鲁棒性等工程局限性未在此片段中详细说明。

#

## 📚 参考文献 (References)

1. Pan, Y.T.; Chou, J.L.; Wei, C.S. MAtt: A manifold attention network for EEG decoding. Adv. Neural Inf. Process. Syst. 2022, 35, 31116–31129.

2. Merlin Praveena, D.; Angelin Sarah, D.; Thomas George, S. Deep learning techniques for EEG signal applications—A review. IETE J. Res. 2022, 68, 3030–3037. [CrossRef]

3. Ho, T.K.K.; Armanfard, N. Self-supervised learning for anomalous channel detection in EEG graphs: Application to seizure analysis. In Proceedings of the AAAI Conference on Artiﬁcial Intelligence 2023, Washington, DC, USA, 7–14 February 2023; Volume 37, pp. 7866–7874.

4. Pinti, P.; Tachtsidis, I.; Hamilton, A.; Hirsch, J.; Aichelburg, C.; Gilbert, S.; Burgess, P.W. The present and future use of functional near-infrared spectroscopy (fNIRS) for cognitive neuroscience. Ann. N. Y. Acad. Sci. 2020, 1464, 5–29. [CrossRef]

5. Scholkmann, F.; Kleiser, S.; Metz, A.J.; Zimmermann, R.; Pavia, J.M.; Wolf, U.; Wolf, M. A review on continuous wave functional near-infrared spectroscopy and imaging instrumentation and methodology. Neuroimage 2014, 85, 6–27. [CrossRef] [PubMed]

6. Fernandez Rojas, R.; Huang, X.; Ou, K.L. A machine learning approach for the identiﬁcation of a biomarker of human pain using fNIRS. Sci. Rep. 2019, 9, 5645. [CrossRef] [PubMed]

7. Lee, S.; Shin, Y.; Kumar, A.; Kim, M.; Lee, H.N. Dry electrode-based fully isolated EEG/fNIRS hybrid brain-monitoring system. IEEE Trans. Biomed. Eng. 2018, 66, 1055–1068. [CrossRef] [PubMed]

8. Ortega, P.; Faisal, A.A. Deep learning multimodal fNIRS and EEG signals for bimanual grip force decoding. J. Neural Eng. 2021, 18, 0460e6. [CrossRef] [PubMed]

9. Schirrmeister, R.T.; Springenberg, J.T.; Fiederer, L.D.J.; Glasstetter, M.; Eggensperger, K.; Tangermann, M.; Hutter, F.; Burgard, W.; Ball, T. Deep learning with convolutional neural networks for EEG decoding and visualization. Hum. Brain Mapp. 2017, 38, 5391–5420. [CrossRef] [PubMed]

10. Lawhern, V.J.; Solon, A.J.; Waytowich, N.R.; Gordon, S.M.; Hung, C.P.; Lance, B.J. EEGNet: A compact convolutional neural network for EEG-based brain–computer interfaces. J. Neural Eng. 2018, 15, 056013. [CrossRef] [PubMed]

11. Acharya, U.R.; Oh, S.L.; Hagiwara, Y.; Tan, J.H.; Adeli, H. Deep convolutional neural network for the automated detection and diagnosis of seizure using EEG signals. Comput. Biol. Med. 2018, 100, 270–278. [CrossRef]

12. Chiarelli, A.M.; Croce, P.; Merla, A.; Zappasodi, F. Deep learning for hybrid EEG-fNIRS brain–computer interface: Application to motor imagery classiﬁcation. J. Neural Eng. 2018, 15, 036028. [CrossRef] Sensors 2024, 24, 1889 15 of 16

13. Shin, J.; Kwon, J.; Im, C.H. A ternary hybrid EEG-NIRS brain-computer interface for the classiﬁcation of brain activation patterns during mental arithmetic, motor imagery, and idle state. Front. Neuroinform. 2018, 12,

5. [CrossRef]

14. Kwak, Y.; Song, W.J.; Kim, S.E. FGANet: FNIRS-guided attention network for hybrid EEG-fNIRS brain-computer interfaces. IEEE Trans. Neural Syst. Rehabil. Eng. 2022, 30, 329–339. [CrossRef] [PubMed]

15. Wang, Y.; Han, Y.; Wang, H.; Zhang, X. Contrast Everything: A Hierarchical Contrastive Framework for Medical Time-Series. In Proceedings of the 37th Annual Conference on Neural Information Processing Systems (NeurIPS 2023), New Orleans, LA, USA, 10–16 December 2023.

16. Lan, X.; Ng, D.; Hong, S.; Feng, M. Intra-inter subject self-supervised learning for multivariate cardiac signals. In Proceedings of the AAAI Conference on Artiﬁcial Intelligence 2022, Online, 22 February–1 March 2022; Volume 36, pp. 4532–4540.

17. Shin, J.; Von Lühmann, A.; Kim, D.W.; Mehnert, J.; Hwang, H.J.; Müller, K.R. Simultaneous acquisition of EEG and NIRS during cognitive tasks for an open access dataset. Sci. Data 2018, 5, 180003. [CrossRef]

18. Zhang, X.; Yao, L.; Wang, X.; Monaghan, J.; Mcalpine, D.; Zhang, Y. A survey on deep learning-based non-invasive brain signals: Recent advances and new frontiers. J. Neural Eng. 2021, 18, 031002. [CrossRef]

19. Dai, G.; Zhou, J.; Huang, J.; Wang, N. HS-CNN: A CNN with hybrid convolution scale for EEG motor imagery classiﬁcation. J. Neural Eng. 2020, 17, 016025. [CrossRef] [PubMed]

20. Ingolfsson, T.M.; Hersche, M.; Wang, X.; Kobayashi, N.; Cavigelli, L.; Benini, L. EEG-TCNet: An accurate temporal convolutional network for embedded motor-imagery brain–machine interfaces. In Proceedings of the 2020 IEEE International Conference on Systems, Man, and Cybernetics (SMC), Toronto, ON, Canada, 11–14 October 2020; pp. 2958–2965.

21. Eastmond, C.; Subedi, A.; De, S.; Intes, X. Deep learning in fNIRS: A review. Neurophotonics 2022, 9, 041411. [CrossRef]

22. Çetinta¸s, D.; Firat, T.T. Eye-tracking analysis with deep learning method. In Proceedings of the 2021 International Conference on Innovation and Intelligence for Informatics, Computing, and Technologies (3ICT), Zallaq, Bahrain, 29–30 September 2021; pp. 512–515.

23. Katona, J. Analyse the readability of LINQ code using an eye-tracking-based evaluation. Acta Polytech. Hung 2021, 18, 193–215. [CrossRef]

24. Wang, M.; Lyu, X.Q.; Li, Y.J.; Zhang, F.L. VR content creation and exploration with deep learning: A survey. Comput. Vis. Media 2020, 6, 3–28. [CrossRef]

25. Fang, B.; Ding, W.; Sun, F.; Shan, J.; Wang, X.; Wang, C.; Zhang, X. Brain-computer interface integrated with augmented reality for human-robot interaction. IEEE Trans. Cogn. Dev. Syst. 2022, 15, 1702–1711. [CrossRef]

26. Karácsony, T.; Hansen, J.P.; Iversen, H.K.; Puthusserypady, S. Brain computer interface for neuro-rehabilitation with deep learning classiﬁcation and virtual reality feedback. In Proceedings of the 10th Augmented Human International Conference 2019, Reims, France, 11–12 March 2019; pp. 1–8.

27. Karamians, R.; Profﬁtt, R.; Kline, D.; Gauthier, L.V. Effectiveness of virtual reality-and gaming-based interventions for upper extremity rehabilitation poststroke: A meta-analysis. Arch. Phys. Med. Rehabil. 2020, 101, 885–896. [CrossRef]

28. Sriram, H.; Conati, C.; Field, T. Classiﬁcation of Alzheimer’s Disease with Deep Learning on Eye-tracking Data. In Proceedings of the 25th International Conference on Multimodal Interaction, Paris, France, 9–13 October 2023; pp. 104–113.

29. Zuo, F.; Jing, P.; Sun, J.; Duan, J.; Ji, Y.; Liu, Y. Deep Learning-based Eye-Tracking Analysis for Diagnosis of Alzheimer’s Disease Using 3D Comprehensive Visual Stimuli. IEEE J. Biomed. Health Inform. 2024. [CrossRef]

30. Rivera, M.J.; Teruel, M.A.; Mate, A.; Trujillo, J. Diagnosis and prognosis of mental disorders by means of EEG and deep learning: A systematic mapping study. Artif. Intell. Rev. 2022, 55, 1209–1251. [CrossRef]

31. Jafari, M.; Shoeibi, A.; Khodatars, M.; Bagherzadeh, S.; Shalbaf, A.; García, D.L.; Gorriz, J.M.; Acharya, U.R. Emotion recognition in EEG signals using deep learning methods: A review. Comput. Biol. Med. 2023, 165, 107450. [CrossRef] [PubMed]

32. Deligani, R.J.; Borgheai, S.B.; McLinden, J.; Shahriari, Y. Multimodal fusion of EEG-fNIRS: A mutual information-based hybrid classiﬁcation framework. Biomed. Opt. Express 2021, 12, 1635–1650. [CrossRef] [PubMed]

33. Shin, J.; von Lühmann, A.; Blankertz, B.; Kim, D.W.; Jeong, J.; Hwang, H.J.; Müller, K.R. Open access dataset for EEG+ NIRS single-trial classiﬁcation. IEEE Trans. Neural Syst. Rehabil. Eng. 2016, 25, 1735–1745. [CrossRef] [PubMed]

34. Fazli, S.; Mehnert, J.; Steinbrink, J.; Curio, G.; Villringer, A.; Müller, K.R.; Blankertz, B. Enhanced performance by a hybrid NIRS–EEG brain computer interface. Neuroimage 2012, 59, 519–529. [CrossRef]

35. Alhudhaif, A. An effective classiﬁcation framework for brain-computer interface system design based on combining of fNIRS and EEG signals. PeerJ Comput. Sci. 2021, 7, e537. [CrossRef] [PubMed]

36. Li, R.; Potter, T.; Huang, W.; Zhang, Y. Enhancing performance of a hybrid EEG-fNIRS system using channel selection and early temporal features. Front. Hum. Neurosci. 2017, 11,

462. [CrossRef] [PubMed]

37. Aghajani, H.; Garbey, M.; Omurtag, A. Measuring mental workload with EEG+ fNIRS. Front. Hum. Neurosci. 2017, 11,

359. [CrossRef]

38. He, Q.; Feng, L.; Jiang, G.; Xie, P. Multimodal multitask neural network for motor imagery classiﬁcation with EEG and fNIRS signals. IEEE Sens. J. 2022, 22, 20695–20706. [CrossRef]

39. Cooney, C.; Folli, R.; Coyle, D. A bimodal deep learning architecture for EEG-fNIRS decoding of overt and imagined speech. IEEE Trans. Biomed. Eng. 2021, 69, 1983–1994. [CrossRef] [PubMed]

40. Sirpal, P.; Kassab, A.; Pouliot, P.; Nguyen, D.K.; Lesage, F. fNIRS improves seizure detection in multimodal EEG-fNIRS recordings. J. Biomed. Opt. 2019, 24, 051408. [CrossRef] [PubMed] Sensors 2024, 24, 1889 16 of 16

41. Hackeling, G. Mastering Machine Learning with Scikit-Learn; Packt Publishing Ltd.: Birmingham, UK, 2017.

42. Singh, P.; Manure, A.; Singh, P.; Manure, A. Introduction to tensorﬂow 2.0. Learn TensorFlow 2.0: Implement Machine Learning and Deep Learning Models with Python; Apress: New York, NY, USA, 2020; pp. 1–24.

43. Srivastava, N.; Hinton, G.; Krizhevsky, A.; Sutskever, I.; Salakhutdinov, R. Dropout: A simple way to prevent neural networks from overﬁtting. J. Mach. Learn. Res. 2014, 15, 1929–1958.

44. Ioffe, S.; Szegedy, C. Batch normalization: Accelerating deep network training by reducing internal covariate shift. In Proceedings of the International Conference on Machine Learning. PMLR 2015, Lille, France, 6–11 July 2015; pp. 448–456.

45. Agarap, A.F. Deep learning using rectiﬁed linear units (relu). arXiv 2018, arXiv:1803.08375.

46. He, K.; Zhang, X.; Ren, S.; Sun, J. Deep residual learning for image recognition. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition 2016, Las Vegas, NV, USA, 27–30 June 2016; pp. 770–778.

47. Simonyan, K.; Zisserman, A. Very deep convolutional networks for large-scale image recognition. arXiv 2014, arXiv:1409.1556.

48. Vaswani, A.; Shazeer, N.; Parmar, N.; Uszkoreit, J.; Jones, L.; Gomez, A.N.; Kaiser, Ł.; Polosukhin, I. Attention is all you need. In Proceedings of the 31st Annual Conference on Neural Information Processing Systems (NIPS 2017), Long Beach, CA, USA, 4–9 December 2017.

49. Zhou, H.; Zhang, S.; Peng, J.; Zhang, S.; Li, J.; Xiong, H.; Zhang, W. Informer: Beyond efﬁcient transformer for long sequence time-series forecasting. In Proceedings of the AAAI Conference on Artiﬁcial Intelligence 2021, Online, 2–9 February 2021; Volume 35, pp. 11106–11115.

50. Nie, Y.; Nguyen, N.H.; Sinthong, P.; Kalagnanam, J. A Time Series is Worth 64 Words: Long-term Forecasting with Transformers. In Proceedings of the International Conference on Learning Representations 2023, Kigali, Rwanda, 1–5 May 2023. Disclaimer/Publisher’s Note: The statements, opinions and data contained in all publications are solely those of the individual author(s) and contributor(s) and not of MDPI and/or the editor(s). MDPI and/or the editor(s) disclaim responsibility for any injury to people or property resulting from any ideas, methods, instructions or products referred to in the content.