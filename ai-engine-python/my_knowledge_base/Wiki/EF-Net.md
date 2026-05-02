## 📋 元数据 (Metadata)
- **文献题目**：EF-Net: Mental State Recognition by Analyzing Multimodal EEG-fNIRS via CNN
- **文献作者**：Aniqa Arif, Yihe Wang, Rui Yin, Xiang Zhang, Ahmed Helmy
- **发表时间**：2024年3月15日
- **发表地址/期刊会议**：Sensors 2024, 24, 1889 (MDPI期刊)
- **开源代码地址**：未提及

## 📖 论文摘要 (Abstract 中文翻译)
脑信号分析对于研究心理状态及各种神经系统疾病至关重要。测量脑活动最常用的两种非侵入性信号是脑电图（EEG）和功能性近红外光谱（fNIRS）。EEG以其较高的采样频率为特征，能够捕获更多的时间特征；而fNIRS具有更多的通道，能够提供更丰富的空间信息。尽管已有少数研究探索了使用多模态深度学习模型来分析EEG和fNIRS的脑活动，但受试者独立（subject-independent）的训练-测试划分分析仍未得到充分探索。受试者独立设置的结果直接反映了模型在未见受试者上的能力，这对实际应用至关重要。在本文中，我们提出了一种基于CNN的新型多模态深度学习模型EF-Net。我们在EEG-fNIRS词语生成（WG）数据集上对EF-Net进行心理状态识别任务的评估，主要聚焦于受试者独立设置。为保证完整性，我们同时报告了受试者依赖（subject-dependent）和受试者半依赖（subject-semidependent）设置下的结果。我们将本模型与五种基线方法进行了对比，包括三种传统机器学习方法和两种深度学习方法。EF-Net在准确率和F1分数上均展现出优越的性能，全面超越了这些基线。我们的模型在受试者依赖、受试者半依赖和受试者独立设置下分别取得了99.36%、98.31%和65.05%的F1分数，分别比最佳基线的F1分数高出1.83%、4.34%和2.13%。这些结果突显了EF-Net在不同受试者及未见受试者中有效学习并解读心理状态与脑活动的能力。

## 🔍 特征提取项
### 算法结构
EF-Net (EEG-fNIRS Fusion Network) 是一种专为**多模态脑信号分析**设计的轻量级卷积神经网络（CNN）。该模型采用**端到端（End-to-End）**深度学习范式，旨在摒弃传统脑机接口研究中繁琐的“手工特征提取”环节，直接从原始或预处理后的信号中联合学习高层表征。其核心架构逻辑与设计哲学可划分为以下三个阶段：

1. **双模态输入与并行特征提取**：模型并行接收两种模态数据，利用 CNN 的层级卷积操作分别挖掘其固有特性。
   - **EEG 分支（时间动态主导）**：利用 EEG 高采样率优势，网络侧重于捕捉脑电信号在**时间维度**上的快速变化、节律特征与瞬时神经电活动爆发。
   - **fNIRS 分支（空间分布主导）**：利用 fNIRS 多通道优势，网络侧重于捕捉血液动力学响应在**空间维度**上的分布模式、拓扑结构与持续代谢响应。
   - **机制**：通过多层卷积自动过滤噪声并提取局部时空模式（Local Spatiotemporal Patterns），无需依赖功率谱密度（PSD）或小波变换等传统人工先验特征。
2. **多模态融合机制（时空互补）**：模型并非简单拼接原始信号，而是通过特征级融合实现 **EEG 高时间分辨率** 与 **fNIRS 高空间分辨率** 的优势互补。融合后的特征向量能够同时表征电活动的瞬时性与血流代谢的持续性，从而构建出更鲁棒、更具判别力的“心理状态”联合表征。该设计在结构上充分考虑了不同受试者间的生理差异，有助于缓解跨个体信号分布偏移问题。
3. **任务导向分类头**：提取并融合后的多模态高级特征最终输入至全连接层或分类器，用于完成心理状态识别（Mental State Recognition）任务（如词语生成任务中的特定认知状态判定）。

> 💡 **架构细节提示**：由于当前文档主要记录核心设计逻辑，未逐层列出具体参数（如卷积核尺寸、通道数、激活函数类型 ReLU/ELU、池化策略等）。若需进行代码复现或深入剖析网络拓扑，建议查阅原论文 `Methodology` 章节及核心架构图表（通常为 Figure 2 或 Table 1）。

### 训练数据集
- **数据集名称/类型**：EEG-fNIRS 词语生成（Word Generation, WG）数据集。
- **数据模态**：同步采集的多模态脑信号，包含 EEG（脑电图）与 fNIRS（功能性近红外光谱）数据。
- **任务设定**：心理状态识别（Mental State Recognition）。该任务通过分析受试者在执行词语生成任务时的脑活动模式，识别其特定的认知或心理状态。数据集被划分为三种评估协议以全面检验模型泛化能力：受试者依赖（训练集与测试集包含相同受试者）、受试者半依赖（部分重叠或跨会话划分）、受试者独立（训练集与测试集受试者完全无重叠）。

### 训练结果表现
模型在三种不同数据划分协议下均取得了优于基线方法的结果，具体表现如下：
- **受试者依赖设置**：F1分数达到 99.36%，超越最佳基线 1.83%。
- **受试者半依赖设置**：F1分数达到 98.31%，超越最佳基线 4.34%。
- **受试者独立设置**：F1分数达到 65.05%，超越最佳基线 2.13%。
- **综合对比**：在与包含3种传统机器学习方法和2种深度学习方法的5个基线模型对比中，EF-Net 在准确率（Accuracy）和 F1 分数（F1 Score）两项核心指标上均表现出显著优势，证明了其在跨受试者泛化方面的有效性。

### 创新点
1. **聚焦受试者独立泛化评估**：现有脑活动分析研究多集中于受试者依赖或半依赖设置，导致模型在实际部署中面对新受试者时性能骤降。本文率先将研究重心放在受试者独立（Subject-Independent）协议上，直接验证模型对未见受试者的泛化能力，显著提升了算法的现实应用价值。
2. **轻量化多模态CNN融合架构**：提出 EF-Net，通过单一CNN框架高效融合 EEG 的时间动态特征与 fNIRS 的空间血流动力学特征，避免了复杂的手工特征工程，实现了端到端的联合表征学习。轻量化设计不仅降低了计算成本，也有助于在数据量有限的脑科学数据集上防止过拟合。
3. **系统性跨协议基准测试**：在同一数据集上同时报告依赖、半依赖与独立三种设置下的结果，为脑机接口/神经解码领域的模型泛化能力评估提供了更严谨、可复现的对比基准。

### 局限性
1. **跨受试者泛化性能仍有显著下降**：在受试者独立设置下，F1分数降至 65.05%（相比依赖设置的 99.36% 存在较大落差），表明当前模型在应对个体生理差异、脑结构异质性以及信号分布偏移时仍存在瓶颈。
2. **低信噪比与个体特异性干扰**：原文指出，脑信号本身信噪比（Information-to-Noise Ratio）较低，且每个受试者具有独特的神经活动模式。即使标签相同，不同受试者的数据分布也可能存在显著差异，这极大增加了提取通用跨主体特征的难度。
3. **任务与模态的单一性**：当前验证仅基于词语生成（WG）任务，未来需扩展至更多样化的认知任务（如情绪识别、运动想象等）以验证架构的普适性。同时，fNIRS 易受头皮血流、运动伪影干扰，EEG 易受肌电/眼电干扰，模型对复杂真实环境噪声的鲁棒性仍需进一步验证。

#

## 📚 参考文献 (References)

1. Pan,Y.T.; Chou,J.L.; Wei,C.S.MAtt: AmanifoldattentionnetworkforEEGdecoding. Adv. NeuralInf. Process. Syst. 2022, 35,31116–31129.

2. MerlinPraveena,D.;AngelinSarah,D.;ThomasGeorge,S.DeeplearningtechniquesforEEGsignalapplications—Areview. IETEJ.Res.2022,68,3030–3037.[CrossRef]

3. Ho,T.K.K.;Armanfard,N.Self-supervisedlearningforanomalouschanneldetectioninEEGgraphs: Applicationtoseizure analysis. InProceedingsoftheAAAIConferenceonArtificialIntelligence2023,Washington,DC,USA,7–14February2023; Volume37,pp.7866–7874.

4. Pinti,P.;Tachtsidis,I.;Hamilton,A.;Hirsch,J.;Aichelburg,C.;Gilbert,S.;Burgess,P.W.Thepresentandfutureuseoffunctional near-infraredspectroscopy(fNIRS)forcognitiveneuroscience.Ann.N.Y.Acad.Sci.2020,1464,5–29.[CrossRef]

5. Scholkmann,F.;Kleiser,S.;Metz,A.J.;Zimmermann,R.;Pavia,J.M.;Wolf,U.;Wolf,M.Areviewoncontinuouswavefunctional near-infraredspectroscopyandimaginginstrumentationandmethodology.Neuroimage2014,85,6–27.[CrossRef][PubMed]

6. FernandezRojas,R.;Huang,X.;Ou,K.L.Amachinelearningapproachfortheidentificationofabiomarkerofhumanpainusing fNIRS.Sci.Rep.2019,9,5645.[CrossRef][PubMed]

7. Lee,S.;Shin,Y.;Kumar,A.;Kim,M.;Lee,H.N.Dryelectrode-basedfullyisolatedEEG/fNIRShybridbrain-monitoringsystem. IEEETrans.Biomed.Eng.2018,66,1055–1068.[CrossRef][PubMed]

8. Ortega,P.;Faisal,A.A.DeeplearningmultimodalfNIRSandEEGsignalsforbimanualgripforcedecoding.J.NeuralEng.2021, 18,0460e6.[CrossRef][PubMed]

9. Schirrmeister,R.T.;Springenberg,J.T.;Fiederer,L.D.J.;Glasstetter,M.;Eggensperger,K.;Tangermann,M.;Hutter,F.;Burgard, W.;Ball,T.DeeplearningwithconvolutionalneuralnetworksforEEGdecodingandvisualization. Hum. BrainMapp. 2017, 38,5391–5420.[CrossRef][PubMed]

10. Lawhern,V.J.;Solon,A.J.;Waytowich,N.R.;Gordon,S.M.;Hung,C.P.;Lance,B.J.EEGNet: Acompactconvolutionalneural networkforEEG-basedbrain–computerinterfaces.J.NeuralEng.2018,15,056013.[CrossRef][PubMed]

11. Acharya,U.R.;Oh,S.L.;Hagiwara,Y.;Tan,J.H.;Adeli,H.Deepconvolutionalneuralnetworkfortheautomateddetectionand diagnosisofseizureusingEEGsignals.Comput.Biol.Med.2018,100,270–278.[CrossRef]

12. Chiarelli,A.M.;Croce,P.;Merla,A.;Zappasodi,F.DeeplearningforhybridEEG-fNIRSbrain–computerinterface:Applicationto motorimageryclassification.J.NeuralEng.2018,15,036028.[CrossRef][PubMed] Sensors2024,24,1889 15of16

13. Shin,J.;Kwon,J.;Im,C.H.AternaryhybridEEG-NIRSbrain-computerinterfacefortheclassificationofbrainactivationpatterns duringmentalarithmetic,motorimagery,andidlestate.Front.Neuroinform.2018,12,5.[CrossRef]

14. Kwak,Y.;Song,W.J.;Kim,S.E.FGANet:FNIRS-guidedattentionnetworkforhybridEEG-fNIRSbrain-computerinterfaces.IEEE Trans.NeuralSyst.Rehabil.Eng.2022,30,329–339.[CrossRef][PubMed]

15. Wang,Y.;Han,Y.;Wang,H.;Zhang,X.ContrastEverything:AHierarchicalContrastiveFrameworkforMedicalTime-Series.In Proceedingsofthe37thAnnualConferenceonNeuralInformationProcessingSystems(NeurIPS2023),NewOrleans,LA,USA, 10–16December2023.

16. Lan,X.;Ng,D.;Hong,S.;Feng,M.Intra-intersubjectself-supervisedlearningformultivariatecardiacsignals.InProceedingsof theAAAIConferenceonArtificialIntelligence2022,Online,22February–1March2022;Volume36,pp.4532–4540.

17. Shin,J.;VonLühmann,A.;Kim,D.W.;Mehnert,J.;Hwang,H.J.;Müller,K.R.SimultaneousacquisitionofEEGandNIRSduring cognitivetasksforanopenaccessdataset.Sci.Data2018,5,180003.[CrossRef]

18. Zhang,X.;Yao,L.;Wang,X.;Monaghan,J.;Mcalpine,D.;Zhang,Y.Asurveyondeeplearning-basednon-invasivebrainsignals: Recentadvancesandnewfrontiers.J.NeuralEng.2021,18,031002.[CrossRef]

19. Dai,G.;Zhou,J.;Huang,J.;Wang,N.HS-CNN:ACNNwithhybridconvolutionscaleforEEGmotorimageryclassification.J. NeuralEng.2020,17,016025.[CrossRef][PubMed]

20. Ingolfsson,T.M.;Hersche,M.;Wang,X.;Kobayashi,N.;Cavigelli,L.;Benini,L.EEG-TCNet:Anaccuratetemporalconvolutional networkforembeddedmotor-imagerybrain–machineinterfaces.InProceedingsofthe2020IEEEInternationalConferenceon Systems,Man,andCybernetics(SMC),Toronto,ON,Canada,11–14October2020;pp.2958–2965.

21. Eastmond,C.;Subedi,A.;De,S.;Intes,X.DeeplearninginfNIRS:Areview.Neurophotonics2022,9,041411.[CrossRef]

22. Çetintas¸,D.;Firat,T.T.Eye-trackinganalysiswithdeeplearningmethod.InProceedingsofthe2021InternationalConference onInnovationandIntelligenceforInformatics,Computing,andTechnologies(3ICT),Zallaq,Bahrain,29–30September2021; pp.512–515.

23. Katona,J.AnalysethereadabilityofLINQcodeusinganeye-tracking-basedevaluation.ActaPolytech.Hung2021,18,193–213. [CrossRef]

24. Wang,M.;Lyu,X.Q.;Li,Y.J.;Zhang,F.L.VRcontentcreationandexplorationwithdeeplearning:Asurvey.Comput.Vis.Media 2020,6,3–28.[CrossRef]

25. Fang,B.;Ding,W.;Sun,F.;Shan,J.;Wang,X.;Wang,C.;Zhang,X.Brain-computerinterfaceintegratedwithaugmentedrealityfor human-robotinteraction.IEEETrans.Cogn.Dev.Syst.2022,15,1702–1711.[CrossRef]

26. Karácsony,T.;Hansen,J.P.;Iversen,H.K.;Puthusserypady,S.Braincomputerinterfaceforneuro-rehabilitationwithdeeplearning classificationandvirtualrealityfeedback.InProceedingsofthe10thAugmentedHumanInternationalConference2019,Reims, France,11–12March2019;pp.1–8.

27. Karamians,R.;Proffitt,R.;Kline,D.;Gauthier,L.V.Effectivenessofvirtualreality-andgaming-basedinterventionsforupper extremityrehabilitationpoststroke:Ameta-analysis.Arch.Phys.Med.Rehabil.2020,101,885–896.[CrossRef]

28. Sriram,H.;Conati,C.;Field,T.ClassificationofAlzheimer’sDiseasewithDeepLearningonEye-trackingData.InProceedingsof the25thInternationalConferenceonMultimodalInteraction,Paris,France,9–13October2023;pp.104–113.

29. Zuo,F.;Jing,P.;Sun,J.;Duan,J.;Ji,Y.;Liu,Y.DeepLearning-basedEye-TrackingAnalysisforDiagnosisofAlzheimer’sDisease Using3DComprehensiveVisualStimuli.IEEEJ.Biomed.HealthInform.2024.[CrossRef]

30. Rivera,M.J.;Teruel,M.A.;Mate,A.;Trujillo,J.DiagnosisandprognosisofmentaldisordersbymeansofEEGanddeeplearning: Asystematicmappingstudy.Artif.Intell.Rev.2022,55,1209–1251.[CrossRef]

31. Jafari,M.;Shoeibi,A.;Khodatars,M.;Bagherzadeh,S.;Shalbaf,A.;García,D.L.;Gorriz,J.M.;Acharya,U.R.Emotionrecognition inEEGsignalsusingdeeplearningmethods:Areview.Comput.Biol.Med.2023,165,107450.[CrossRef][PubMed]

32. Deligani,R.J.;Borgheai,S.B.;McLinden,J.;Shahriari,Y.MultimodalfusionofEEG-fNIRS:Amutualinformation-basedhybrid classificationframework.Biomed.Opt.Express2021,12,1635–1650.[CrossRef][PubMed]

33. Shin,J.;vonLühmann,A.;Blankertz,B.;Kim,D.W.;Jeong,J.;Hwang,H.J.;Müller,K.R.OpenaccessdatasetforEEG+NIRS single-trialclassification.IEEETrans.NeuralSyst.Rehabil.Eng.2016,25,1735–1745.[CrossRef][PubMed]

34. Fazli,S.; Mehnert,J.; Steinbrink,J.; Curio,G.; Villringer,A.; Müller,K.R.; Blankertz,B.Enhancedperformancebyahybrid NIRS–EEGbraincomputerinterface.Neuroimage2012,59,519–529.[CrossRef]

35. Alhudhaif,A.Aneffectiveclassificationframeworkforbrain-computerinterfacesystemdesignbasedoncombiningoffNIRS andEEGsignals.PeerJComput.Sci.2021,7,e537.[CrossRef][PubMed]

36. Li,R.;Potter,T.;Huang,W.;Zhang,Y.EnhancingperformanceofahybridEEG-fNIRSsystemusingchannelselectionandearly temporalfeatures.Front.Hum.Neurosci.2017,11,462.[CrossRef][PubMed]

37. Aghajani,H.;Garbey,M.;Omurtag,A.MeasuringmentalworkloadwithEEG+fNIRS.Front. Hum. Neurosci. 2017,11,359. [CrossRef]

38. He,Q.;Feng,L.;Jiang,G.;Xie,P.MultimodalmultitaskneuralnetworkformotorimageryclassificationwithEEGandfNIRS signals.IEEESens.J.2022,22,20695–20706.[CrossRef]

39. Cooney,C.;Folli,R.;Coyle,D.AbimodaldeeplearningarchitectureforEEG-fNIRSdecodingofovertandimaginedspeech. IEEETrans.Biomed.Eng.2021,69,1983–1994.[CrossRef][PubMed]

40. Sirpal,P.;Kassab,A.;Pouliot,P.;Nguyen,D.K.;Lesage,F.fNIRSimprovesseizuredetectioninmultimodalEEG-fNIRSrecordings. J.Biomed.Opt.2019,24,051408.[CrossRef][PubMed] Sensors2024,24,1889 16of16

41. Hackeling,G.MasteringMachineLearningwithScikit-Learn;PacktPublishingLtd.:Birmingham,UK,2017.

42. Singh,P.;Manure,A.;Singh,P.;Manure,A.Introductiontotensorflow2.0.LearnTensorFlow2.0:ImplementMachineLearningand DeepLearningModelswithPython;Apress:NewYork,NY,USA,2020;pp.1–24.

43. Srivastava,N.;Hinton,G.;Krizhevsky,A.;Sutskever,I.;Salakhutdinov,R.Dropout:Asimplewaytopreventneuralnetworks fromoverfitting.J.Mach.Learn.Res.2014,15,1929–1953.

44. Ioffe,S.;Szegedy,C.Batchnormalization:Acceleratingdeepnetworktrainingbyreducinginternalcovariateshift.InProceedings oftheInternationalConferenceonMachineLearning.PMLR2015,Lille,France,6–11July2015;pp.448–456.

45. Agarap,A.F.Deeplearningusingrectifiedlinearunits(relu).arXiv2018,arXiv:1803.08375.

46. He,K.; Zhang,X.; Ren,S.; Sun,J.Deepresiduallearningforimagerecognition. InProceedingsoftheIEEEConferenceon ComputerVisionandPatternRecognition2016,LasVegas,NV,USA,27–30June2016;pp.770–778.

47. Simonyan,K.;Zisserman,A.Verydeepconvolutionalnetworksforlarge-scaleimagerecognition.arXiv2014,arXiv:1409.1556.

48. Vaswani,A.;Shazeer,N.;Parmar,N.;Uszkoreit,J.;Jones,L.;Gomez,A.N.;Kaiser,Ł.;Polosukhin,I.Attentionisallyouneed. InProceedingsofthe31stAnnualConferenceonNeuralInformationProcessingSystems(NIPS2017),LongBeach,CA,USA, 4–9December2017.

49. Zhou,H.;Zhang,S.;Peng,J.;Zhang,S.;Li,J.;Xiong,H.;Zhang,W.Informer:Beyondefficienttransformerforlongsequence time-series forecasting. In Proceedings of the AAAI Conference on Artificial Intelligence 2021, Online, 2–9 February 2021; Volume35,pp.11106–11115.

50. Nie,Y.;Nguyen,N.H.;Sinthong,P.;Kalagnanam,J.ATimeSeriesisWorth64Words:Long-termForecastingwithTransformers. InProceedingsoftheInternationalConferenceonLearningRepresentations2023,Kigali,Rwanda,1–5May2023. Disclaimer/Publisher’s Note: The statements, opinions and data contained in all publications are solely those of the individual author(s)andcontributor(s)andnotofMDPIand/ortheeditor(s).MDPIand/ortheeditor(s)disclaimresponsibilityforanyinjuryto peopleorpropertyresultingfromanyideas,methods,instructionsorproductsreferredtointhecontent.