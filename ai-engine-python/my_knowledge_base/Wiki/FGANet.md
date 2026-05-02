## 📋 元数据 (Metadata)
- **文献题目**：FGANet: fNIRS-Guided Attention Network for Hybrid EEG-fNIRS Brain-Computer Interfaces
- **文献作者**：Youngchul Kwak, Woo-Jin Song, Seong-Eun Kim
- **发表时间**：2022年2月7日（在线发表）/ 2022年2月16日（当前版本）
- **发表地址/期刊会议**：IEEE TRANSACTIONS ON NEURAL SYSTEMS AND REHABILITATION ENGINEERING, VOL. 30, 2022
- **开源代码地址**：未提及

## 📖 论文摘要 (Abstract 中文翻译)
非侵入式脑机接口（BCI）已广泛用于神经解码，通过将神经信号连接起来以控制外部设备。BCI系统可允许个体操作辅助设备，如机械臂、轮椅和拼写系统。此外，BCI系统还可用于克服独立EEG和独立fNIRS BCI系统的局限性，以检测癫痫和阿尔茨海默病等神经系统疾病。使用脑电图（EEG）和功能近红外光谱（fNIRS）的混合BCI系统因其在检测神经系统疾病方面的潜力而受到广泛关注。然而，由于EEG和fNIRS在时间分辨率和记录位置上存在差异，大多数混合EEG-fNIRS BCI研究都集中在后期融合（late fusion）策略上。尽管混合BCI的性能有所提升，但后期融合方法在提取EEG和fNIRS信号中的相关特征方面仍存在困难。因此，在本研究中，我们提出了一种基于深度学习的早期融合（early fusion）结构，该结构在全连接层之前融合两种信号，称为fNIRS引导注意力网络（FGANet）。首先，将一维EEG和fNIRS信号转换为三维EEG和fNIRS张量，以便在同一时间点对两种信号进行空间对齐。所提出的fNIRS引导注意力层基于神经血管耦合机制提取EEG和fNIRS张量的联合表征，其中从fNIRS信号中识别出空间重要区域，并从EEG信号中提取详细的神经模式。最后，通过对EEG特征和fNIRS引导注意力特征的预测分数进行加权求和来获得最终预测，以缓解因fNIRS响应延迟而导致的性能下降。实验结果表明，FGANet显著优于独立EEG网络。此外，在心理算术和运动想象任务中，FGANet的准确率分别比最先进算法高出4.0%和2.7%。

## 🔍 特征提取项
### 算法结构
- **核心架构**：提出了一种名为FGANet（fNIRS-Guided Attention Network）的深度学习早期融合网络。
- **数据预处理与对齐**：将原始的一维（1D）EEG和fNIRS时间序列信号转换为三维（3D）张量，实现在同一时间点上的空间对齐。
- **fNIRS引导注意力层**：基于神经血管耦合原理设计。该层利用fNIRS信号的空间敏感性来识别大脑中空间重要区域，并以此引导EEG信号提取高时间分辨率的详细神经活动模式，从而生成联合表征。
- **延迟补偿与决策融合**：在全连接层之后，通过对EEG分支和fNIRS引导注意力分支的预测得分进行加权求和，生成最终预测结果。该加权机制专门用于缓解fNIRS血流动力学响应延迟带来的性能衰减问题。

### 训练数据集
- 提供的文本片段中未明确提及具体的数据集名称、采集设备参数、受试者数量或数据划分比例。
- 仅明确指出模型在两项经典BCI任务上进行了验证与训练：**心理算术（mental arithmetic）**任务与**运动想象（motor imagery）**任务。

### 训练结果表现
- **基线对比**：FGANet的性能显著优于仅使用EEG信号的独立网络（EEG-standalone network）。
- **SOTA对比**：在心理算术任务中，准确率比现有最先进算法高出4.0%；在运动想象任务中，准确率比现有最先进算法高出2.7%。
- 整体表明，该早期融合与注意力引导机制能有效提升混合BCI的分类精度与鲁棒性。

### 创新点
1. **早期融合范式转换**：突破传统混合EEG-fNIRS系统依赖后期融合（决策级融合）的局限，首次在全连接层前实现信号级/特征级的早期深度融合，有效捕获跨模态相关性。
2. **神经血管耦合驱动的注意力机制**：创新性地利用fNIRS对空间/血流动力学变化敏感的特性作为“引导器”，指导高时间分辨率的EEG特征提取，实现优势互补。
3. **张量空间对齐技术**：将1D生理信号重构为3D张量，解决了EEG（头皮电极）与fNIRS（光极通道）在物理空间与采样频率上的不一致问题。
4. **延迟感知的加权决策策略**：针对fNIRS固有的血流动力学延迟（通常滞后数秒），设计了加权求和预测机制，有效抑制了响应延迟对实时分类性能的负面影响。

### 局限性
- 提供的文本片段为引言与摘要部分，未包含完整的讨论（Discussion）或局限性分析章节。
- 从背景描述可推断，fNIRS本身仍存在**时间分辨率较低**和**血流动力学响应延迟**的生理固有局限，尽管FGANet通过加权策略进行了缓解，但并未从根本上改变fNIRS的物理测量特性。此外，早期融合结构可能对信号预处理（如伪影去除、时空对齐精度）的要求更高，在跨受试者或复杂运动场景下的泛化能力需进一步验证。

#

## 📚 参考文献 (References)

improving the performance. However, the proposed fusion method, FGANet, outper-

[1] G. Schalk, D. J. McFarland, T. Hinterberger, N. Birbaumer, and formed the state-of-the-art algorithm (IDPF) in both the MA J. R. Wolpaw, “BCI2000: A general-purpose brain-computer interface (BCI) system,” IEEE Trans. Biomed. Eng., vol. 51, no. 6, and MI tasks. More specifically, the maximum accuracy of pp.1034–1043,Jun.2004. FGANet is 4.3% and 1.7% higher than that of the IDPF in

[2] G. Purtscheller and C. Neuper, “Motor imagery and direct brainthe MA and MI tasks, respectively. Furthermore, the mean computer communication,” Proc.IEEE,vol. 89,no.7,pp.1123–1134, accuracy of FGANet was greater than 2% as (p < 0.05) Jul.2001.

[3] J.Wolpawetal.,“Brain-computerinterfacetechnology:Areviewofthe comparedto the pth-PF, and pth-PF (EEG + fNIRS branch), first international meeting,” IEEE Trans. Rehabil. Eng., vol. 8, no. 2, which is the state-of-the-art deep learning-based algorithm pp.164–173,Feb.2000. in both the MA and MI tasks. These results show that our

[4] J.-H. Jeong, K.-H. Shim, D.-J. Kim, and S.-W. Lee, “Brain-controlled robotic arm system based on multi-directional CNN-BiLSTM network fNIRS-guided fusion method can considerably improve the using EEG signals,” IEEE Trans. Neural Syst. Rehabil. Eng., vol. 28, performance of the hybrid EEG-fNIRS BCI system, and is no.5,pp.1226–1238,May2020. applicabletoreal-timeapplications.Furthermore,comparedto

[5] Z.T.Al-Qaysi,B.B.Zaidan,A.A.Zaidan,andM.S.Suzani,“Areview ofdisabilityEEGbasedwheelchaircontrolsystem:Coherenttaxonomy, pth-PF (EEG + fusion branch), the mean and max accuracy open challenges and recommendations,” Comput. Methods Programs of FGANet was significantly higher (p < 0.05). This result Biomed.,vol.164,pp.221–237,Oct.2018. shows the superiority of our prediction method as compared

[6] R.Scherer,G.R.Müller,C.Neuper,B.Graimann,andG.Pfurtscheller, “An asynchronously controlled EEG-based virtual keyboard: Improveto the conventional algorithms. ment of the spelling rate,” IEEE Trans. Biomed. Eng., vol. 51, no. 6, pp.979–984,Jun.2004.

[7] S. Ramgopal et al., “Seizure detection, seizure prediction, and V. CONCLUSION closed-loop warning systems in epilepsy,” Epilepsy Behav., vol. 37, In this study, we proposed the fNIRS-guided attention pp.291–307,Aug.2014.

[8] A. T. Tzallas et al., “Automated epileptic seizure detection methods: network (FGANet) as a deep learning-based early fusion Areviewstudy,”inEpilepsy-Histological,Electroencephalographic and structure. First, the 1D multi-channelEEG and fNIRS signals Psychological Aspects,Feb.2012,pp.75–98. were converted into 3D EEG and fNIRS tensors to spatially

[9] C.Melissant, A.Ypma,E.E.E.Frietman, andC.J.Stam,“Amethod fordetectionofAlzheimer’sdiseaseusingICA-enhancedEEGmeasurealign the EEG and fNIRS signals. Thereafter, we extracted a ments,”Artif.Intell. Med.,vol.33,no.3,pp.209–222,Mar.2005. joint representation of both signals using the proposed FGA

[10] S. Fazli et al., “Enhanced performance by a hybrid NIRS–EEG brain layer. In the FGA layer, fNIRS features were used to create computerinterface,” NeuroImage, vol.59,no.1,pp.519–529,2012.

[11] J. Mellinger et al., “An MEG-based brain–computer interface (BCI),” the FGA mapthatidentifiesthe importantregionsofthe EEG NeuroImage, vol.36,no.3,pp.581–593,Jul.2007. featuresforreliableEEGdecoding.TheFGAmapwastrained

[12] S.H.SardouieandM.B.Shamsollahi,“Selectionofefficientfeaturesfor to maximize the spatial correlation between the EEG features discriminationofhandmovementsfromMEGusingaBCIcompetition IVdataset,”Frontiers Neurosci.,vol.6,p.42,Apr.2012. and the FGA map using FGA map regularization.Finally, the

[13] M.A.Tanveer,M.J.Khan,M.J.Qureshi,N.Naseer,andK.-S.Hong, prediction score of the EEG branch was added to the final “Enhanceddrowsinessdetectionusingdeeplearning:AnfNIRSstudy,” predictiontoalleviatetheperformancedeteriorationcausedby IEEEAccess,vol.7,pp.137920–137929,2019.

[14] T. K. K. Ho, J. Gwak, C. M. Park, and J. Song, “Discrimination of the inherent delay of fNIRS signals. The experimentalresults mental workload levels frommulti-channel fNIRS using deep leaningshowed that our FGANet outperformed ESNet, FSNet, and basedapproaches,” IEEEAccess,vol.7,pp.24392–24403,2019. the state-of-the-art fNIRS-EEG fusion method. Furthermore,

[15] J. Kwon and C.-H. Im, “Performance improvement of near-infrared we verified that the FGA map properly highlighted the spa- spectroscopy-based brain-computer interfaces using transcranial nearinfraredphotobiomodulationwiththesamedevice,”IEEETrans.Neural tially important regions of the EEG features. This framework Syst.Rehabil.Eng.,vol.28,no.12,pp.2608–2614,Dec.2020. KWAKetal.:FGANetFORHYBRIDEEG-fNIRSBRAIN-COMPUTERINTERFACES 339

[16] L.G.Limetal.,“Aunifiedanalytical frameworkwithmultiple fNIRS

[37] C. G. Snoek, M. Worring, and A. W. Smeulders, “Early versus late featuresformentalworkloadassessmentintheprefrontalcortex,”IEEE fusioninsemanticvideoanalysis,”inProc.13thAnnu.ACMInt.Conf. Trans. Neural Syst. Rehabil. Eng., vol. 28, no. 11, pp.2367–2376, Multimedia, Nov.2005,pp.399–402. Nov.2020.

[38] N.Neverova, C.Wolf,G.W.Taylor, andF.Nebout, “Multi-scale deep

[17] S.-S. Yoo et al., “Brain–computer interface using fMRI: Spatial nav- learning for gesture detection and localization,” in Proc. Workshop igation by thoughts,” NeuroReport, vol. 15, no. 10, pp.1591–1595, Eur. Conf. Comput. Vis., Cham, Switzerland: Springer, Sep. 2014, Jul.2004. pp.474–490.

[18] G. Rota, G. Handjaras, R. Sitaram, N. Birbaumer, and G. Dogil,

[39] V. Vielzeuf, A. Lechervy, S. Pateux, and F. Jurie, “Multilevel sensor “Reorganizationoffunctionalandeffectiveconnectivityduringreal-time fusion with deep learning,” IEEE Sensors Lett., vol. 3, no. 1, pp.1–4, fMRI-BCI modulation of prosody processing,” Brain Lang., vol. 117, Jan.2019. no.3,pp.123–132,Jun.2011.

[40] Y.-R. Cho, S. Shin, S.-H. Yim, K. Kong, H.-W.Cho, and W.-J. Song,

[19] G. Pfurtscheller, “The hybrid BCI,” Frontiers Neurosci., vol. 4, p.3, “Multistage fusion with dissimilarity regularization for SAR/IR target Apr.2010. recognition,” IEEEAccess,vol.7,pp.728–740,2019.

[20] J. Shin et al., “Open access dataset for EEG+NIRS single-trial clas-

[41] X. Yang, P. Molchanov, and J. Kautz, “Multilayer and multimodal sification,” IEEE Trans. Neural Syst. Rehabil. Eng., vol. 25, no. 10, fusionofdeepneural networks forvideoclassification,” inProc.ACM pp.1735–1745,Oct.2017. Multimedia Conf.,Oct.2016,pp.978–987.

[21] J. Shin, J. Kwon, and C.-H. Im, “A ternary hybrid EEG-NIRS brain-

[42] C. S. Roy and C. S. Sherrington, “On the regulation of the bloodcomputer interface for the classification of brain activation patterns supply of the brain,” J. Physiol., vol. 11, nos. 1–2, pp.85–158, during mental arithmetic, motor imagery, and idle state,” Frontiers Jan.1890. Neuroinform., vol.12,p.5,Feb.2018.

[43] P. Lachert, D. Janusek, P. Pulawski, A. Liebert, D. Milej, and

[22] F. Al-Shargie, T. B. Tang, and M. Kiguchi, “Stress assessment based K.J.Blinowska, “Coupling of Oxy- and deoxyhemoglobin concentraon decision fusion of EEG and fNIRS signals,” IEEE Access, vol. 5, tions with EEG rhythms during motor task,” Sci. Rep., vol. 7, no. 1, pp.19889–19896,2017. pp.1–9,Nov.2017.

[23] L.-W. Ko et al., “Multimodal fuzzy fusion for enhancing the motor-

[44] M.Takeuchietal.,“Braincortical mappingbysimultaneous recording imagery-based brain computer interface,” IEEE Comput. Intell. Mag., of functional near infrared spectroscopy and electroencephalograms vol.14,no.1,pp.96–106,Feb.2019. from the whole brain during right median nerve stimulation,” Brain

[24] C.-H.Han,K.-R.M´’uller,andH.-J.Hwang,“Enhancedperformanceof Topography, vol.22,no.3,pp.197–214,Aug.2009. a brain switch by simultaneous use of EEG and NIRS data for asyn-

[45] A. Gundel and G. F. Wilson, “Topographical changes in the ongoing chronous brain-computer interface,” IEEETrans.Neural Syst. Rehabil. EEGrelatedtothedifficultyofmentaltasks,”BrainTopography,vol.5, Eng.,vol.28,no.10,pp.2102–2112,Oct.2020. no.1,pp.17–25,1992.

[25] X. Jiang, X. Gu, K. Xu, H. Ren, and W. Chen, “Independent

[46] M. Benedek, R. J. Schickel, E. Jauk, A. Fink, and A. C. Neubauer, decision path fusion for bimodal asynchronous brain–computer inter- “Alphapowerincreases inrightparietal cortexreflectsfocusedinternal face to discriminate multiclass mental states,” IEEE Access, vol. 7, attention,” Neuropsychologia, vol.56,pp.393–400,Apr.2014. pp.165303–165317,2019.

[47] L. Brinkman, A. Stolk, H. C. Dijkerman, F. P. de Lange, and I. Toni,

[26] S. Fazli, J. Mehnert, J. Steinbrink, and B. Blankertz, “Using NIRS as “Distinct roles for Alpha- and beta-band oscillations during mental apredictorforEEG-basedBCIperformance,”inProc.Annu.Int.Conf. simulation of goal-directed actions,” J. Neurosci., vol. 34, no. 44, IEEEEng.Med.Biol.Soc.,Aug.2012,pp.4911–4914. pp.14783–14792,Oct.2014.

[27] H.Moriokaetal.,“Decodingspatialattentionbyusingcorticalcurrents

[48] L. Kocsis, P. Herman, and A. Eke, “The modified beer–lambert estimatedfromelectroencephalography withnear-infrared spectroscopy law revisited,” Phys. Med. Biol., vol. 51, no. 5, pp. N91–N98, priorinformation,” NeuroImage, vol.90,pp.128–139,Apr.2014. Mar.2006.

[28] K.SimonyanandA.Zisserman,“Verydeepconvolutional networksfor

[49] D.Tran,L.Bourdev,R.Fergus,L.Torresani,andM.Paluri,“Learning large-scale imagerecognition,” 2014,arXiv:1409.1556. spatiotemporalfeatureswith3Dconvolutionalnetworks,”inProc.IEEE

[29] K.SimonyanandA.Zisserman,“Verydeepconvolutional networksfor Int.Conf.Comput.Vis.,Dec.2015,pp.4489–4497. large-scale imagerecognition,” 2014,arXiv:1409.1556.

[50] S.Ji,W.Xu,M.Yang, andK.Yu,“3D convolutional neural networks

[30] J. Redmon and A. Farhadi, “YOLOv3: An incremental improvement,” forhumanactionrecognition,”IEEETrans.PatternAnal.Mach.Intell., 2018,arXiv:1804.02767. vol.35,no.1,pp.221–231,Jan.2012.

[31] G.Hintonetal.,“Deepneuralnetworksforacousticmodelinginspeech

[51] N.Srivastava, G.Hinton,A.Krizhevsky,I.Sutskever, andR.Salakhutrecognition: The shared views of four research groups,” IEEE Signal dinov, “Dropout: A simple way to prevent neural networks from overProcess.Mag.,vol.29,no.6,pp.82–97,Nov.2012. fitting,”J.Mach.Learn.Res.,vol.15,no.1,pp.1929–1958,Jan.2014.

[32] A.M.Chiarelli, P.Croce, A.Merla, andF.Zappasodi, “Deeplearning

[52] O.Jensen,J.Gelfand,J.Kounios,andJ.E.Lisman,“Oscillationsinthe forhybridEEG-fNIRSbrain–computer interface: Application tomotor alphaband(9–12Hz)increase withmemoryloadduringretention ina imagery classification,” J. Neural Eng., vol. 15, no. 3, Apr. 2018, short-termmemorytask,”CerebralCortex,vol.12,no.8,pp.877–882, Art.no.036028. 2002.

[33] Z. Sun, Z. Huang, F. Duan, and Y. Liu, “A novel multimodal

[53] D.P.KingmaandJ.Ba,“Adam:Amethodforstochasticoptimization,” approach for hybrid brain–computer interface,” IEEE Access, vol. 8, 2014,arXiv:1412.6980. pp.89909–89918,2020.

[54] E.ErgünandO.Aydemir,“Anewevolutionarypreprocessingapproach

[34] Y.Kwak,K.Kong,W.-J.Song,B.-K.Min,andS.-E.Kim,“Multilevel for classification of mental arithmetic based EEG signals,” Cognit. feature fusion with 3D convolutional neural network for EEG-based Neurodyn.,vol.14,no.5,pp.609–617,Apr.2020. workload estimation,” IEEEAccess,vol.8,pp.16009–16021,2020.

[55] E.ErgünandO.Aydemir,“Decodingofbinarymentalarithmeticbased

[35] X. Zhao, H. Zhang, G. Zhu, F. You, S. Kuang, and L. Sun, “A multi- near-infraredspectroscopysignals,”inProc.3rdInt.Conf.Comput.Sci. branch3Dconvolutional neuralnetworkforEEG-basedmotorimagery Eng.(UBMK),Sep.2018,pp.201–204. classification,” IEEETrans.NeuralSyst.Rehabil.Eng.,vol.27,no.10,

[56] E.ErgunandO.Aydemir,“Classificationofmotorimaginarybasednearpp.2164–2177,Oct.2019. infrared spectroscopy signals,” inProc. 26thSignal Process.Commun.

[36] J.-H. Jeong, K.-H. Shim, D.-J. Kim, and S.-W. Lee, “Brain-controlled Appl.Conf.(SIU),May2018,pp.1–4. robotic arm system based on multi-directional CNN-BiLSTM network

[57] E.A. Aydin, “Subject-specific feature selection fornear infrared specusing EEG signals,” IEEE Trans. Neural Syst. Rehabil. Eng., vol. 28, troscopybasedbrain-computer interfaces,” Comput.MethodsPrograms no.5,pp.1226–1238,May2020. Biomed.,vol.195,Oct.2020,Art.no.105535.