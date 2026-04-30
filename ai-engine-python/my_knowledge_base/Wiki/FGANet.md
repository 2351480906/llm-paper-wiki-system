```markdown
## 科研内容提取（基于 IEEE TNSRE 2022 论文 "FGANet: fNIRS-Guided Attention Network for Hybrid EEG-fNIRS Brain-Computer Interfaces"）

### 🔧 算法结构  
- **整体架构**：端到端深度学习模型，采用**早期融合（early fusion）策略**，在全连接层之前融合EEG与fNIRS模态特征。  
- **信号预处理**：将一维原始EEG和fNIRS时序信号分别转换为**三维张量（3D tensors）**，实现空间对齐（匹配电极/探头位置）与时间同步。  
- **核心模块——fNIRS引导注意力层（fNIRS-guided attention layer）**：  
  - 基于**神经血管耦合机制**（neurovascular coupling），利用fNIRS的血氧动力学响应定位**空间重要脑区**（如高HbO浓度区域）；  
  - 在这些关键区域上对EEG特征进行加权聚焦，从而提取具有生理意义的**联合表征**；  
  - 实现“fNIRS指导空间注意力、EEG提供高时间分辨率神经活动细节”的协同建模。  
- **预测融合**：对EEG分支与fNIRS引导注意力分支的预测得分进行**加权求和**，以缓解fNIRS固有的血流响应延迟（约5–8 s）导致的性能下降。

### 📊 训练数据集  
- **任务类型**：双范式混合BCI任务（mental arithmetic 和 motor imagery）；  
- **模态数据**：同步采集的**多通道EEG + 多通道fNIRS**信号（具体通道数未在摘要中明示，但方法部分提及空间对齐需匹配电极/探头布局）；  
- **数据来源**：论文未在摘要中披露具体公开数据集名称，但实验设计表明使用了**自建或标准混合EEG-fNIRS实验数据集**（典型配置含16–32导EEG + 8–16通道fNIRS）；  
- **标注信息**：按任务类别（如MA vs. rest；MI-left vs. MI-right vs. rest）进行样本级标签。

### 📈 训练结果表现  
- **显著优于单模态基线**：FGANet显著超越纯EEG独立网络（EEG-standalone network）；  
- **SOTA对比优势**：  
  - **精神算术任务（Mental Arithmetic）**：准确率较当时最优算法提升 **+4.0%**；  
  - **运动想象任务（Motor Imagery）**：准确率较当时最优算法提升 **+2.7%**；  
- **关键贡献验证**：早期融合+注意力引导机制有效提升了跨模态特征协同解码能力，尤其在低信噪比、高延迟场景下鲁棒性增强。

### 💡 创新点  
1. **首个fNIRS引导的注意力机制**：首次将fNIRS的**空间特异性血氧响应**显式建模为EEG特征提取的**空间注意力先验**，物理可解释性强；  
2. **面向神经血管耦合的早期融合范式**：突破传统混合BCI依赖晚期融合（late fusion）的局限，提出生理机制驱动的早期特征对齐与融合框架；  
3. **延迟感知预测融合策略**：通过加权融合缓解fNIRS响应滞后问题，提升实时BCI系统的时间一致性；  
4. **3D张量化时空对齐**：将1D时序信号升维为3D张量，统一EEG（电极×时间×trial）与fNIRS（通道×时间×trial）的空间拓扑结构，支撑可学习的空间注意力。

### ⚠️ 局限性  
- **fNIRS时间分辨率限制未根本解决**：虽通过加权融合缓解延迟影响，但无法消除fNIRS固有慢响应特性，制约毫秒级动态神经过程追踪；  
- **个体差异适应性不足**：模型未包含跨被试迁移学习或个性化自适应模块，泛化至新用户时可能需额外校准；  
- **计算与部署开销**：3D张量操作与注意力机制增加参数量与推理延迟，对嵌入式/便携式BCI设备的实时性构成挑战；  
- **生理机制假设依赖性强**：性能高度依赖神经血管耦合的局部一致性假设，在病理人群（如脑卒中、血管畸形）中有效性待验证。

#

## 📚 参考文献

[1] G. Schalk, D. J. McFarland, T. Hinterberger, N. Birbaumer, and J. R. Wolpaw, “BCI2000: A general-purpose brain-computer inter- face (BCI) system,” IEEE Trans. Biomed. Eng., vol. 51, no. 6, pp. 1034–1043, Jun. 

2004. 

[2] G. Purtscheller and C. Neuper, “Motor imagery and direct brain- computer communication,” Proc. IEEE, vol. 89, no. 7, pp. 1123–1134, Jul. 

2001. 

[3] J. Wolpaw et al., “Brain-computer interface technology: A review of the ﬁrst international meeting,” IEEE Trans. Rehabil. Eng., vol. 8, no. 2, pp. 164–173, Feb. 

2000. 

[4] J.-H. Jeong, K.-H. Shim, D.-J. Kim, and S.-W. Lee, “Brain-controlled robotic arm system based on multi-directional CNN-BiLSTM network using EEG signals,” IEEE Trans. Neural Syst. Rehabil. Eng., vol. 28, no. 5, pp. 1226–1238, May 

2020. 

[5] Z. T. Al-Qaysi, B. B. Zaidan, A. A. Zaidan, and M. S. Suzani, “A review of disability EEG based wheelchair control system: Coherent taxonomy, open challenges and recommendations,” Comput. Methods Programs Biomed., vol. 164, pp. 221–237, Oct. 

2018. 

[6] R. Scherer, G. R. Müller, C. Neuper, B. Graimann, and G. Pfurtscheller, “An asynchronously controlled EEG-based virtual keyboard: Improve- ment of the spelling rate,” IEEE Trans. Biomed. Eng., vol. 51, no. 6, pp. 979–984, Jun. 

2004. 

[7] S. Ramgopal et al., “Seizure detection, seizure prediction, and closed-loop warning systems in epilepsy,” Epilepsy Behav., vol. 37, pp. 291–307, Aug. 

2014. 

[8] A. T. Tzallas et al., “Automated epileptic seizure detection methods: A review study,” in Epilepsy-Histological, Electroencephalographic and Psychological Aspects, Feb. 2012, pp. 75–

98. 

[9] C. Melissant, A. Ypma, E. E. E. Frietman, and C. J. Stam, “A method for detection of Alzheimer’s disease using ICA-enhanced EEG measure- ments,” Artif. Intell. Med., vol. 33, no. 3, pp. 209–222, Mar. 

2005. 

[10] S. Fazli et al., “Enhanced performance by a hybrid NIRS–EEG brain computer interface,” NeuroImage, vol. 59, no. 1, pp. 519–529, 

2012. 

[11] J. Mellinger et al., “An MEG-based brain–computer interface (BCI),” NeuroImage, vol. 36, no. 3, pp. 581–593, Jul. 

2007. 

[12] S. H. Sardouie and M. B. Shamsollahi, “Selection of efﬁcient features for discrimination of hand movements from MEG using a BCI competition IV data set,” Frontiers Neurosci., vol. 6, p. 42, Apr. 

2012. 

[13] M. A. Tanveer, M. J. Khan, M. J. Qureshi, N. Naseer, and K.-S. Hong, “Enhanced drowsiness detection using deep learning: An fNIRS study,” IEEE Access, vol. 7, pp. 137920–137929, 

2019. 

[14] T. K. K. Ho, J. Gwak, C. M. Park, and J. Song, “Discrimination of mental workload levels from multi-channel fNIRS using deep leaning- based approaches,” IEEE Access, vol. 7, pp. 24392–24403, 

2019. 

[15] J. Kwon and C.-H. Im, “Performance improvement of near-infrared spectroscopy-based brain-computer interfaces using transcranial near- infrared photobiomodulation with the same device,” IEEE Trans. Neural Syst. Rehabil. Eng., vol. 28, no. 12, pp. 2608–2614, Dec. 

2020. KWAK et al.: FGANet FOR HYBRID EEG-fNIRS BRAIN-COMPUTER INTERFACES 339 

[16] L. G. Lim et al., “A uniﬁed analytical framework with multiple fNIRS features for mental workload assessment in the prefrontal cortex,” IEEE Trans. Neural Syst. Rehabil. Eng., vol. 28, no. 11, pp. 2367–2376, Nov. 

2020. 

[17] S.-S. Yoo et al., “Brain–computer interface using fMRI: Spatial nav- igation by thoughts,” NeuroReport, vol. 15, no. 10, pp. 1591–1595, Jul. 

2004. 

[18] G. Rota, G. Handjaras, R. Sitaram, N. Birbaumer, and G. Dogil, “Reorganization of functional and effective connectivity during real-time fMRI-BCI modulation of prosody processing,” Brain Lang., vol. 117, no. 3, pp. 123–132, Jun. 

2011. 

[19] G. Pfurtscheller, “The hybrid BCI,” Frontiers Neurosci., vol. 4, p. 3, Apr. 

2010. 

[20] J. Shin et al., “Open access dataset for EEG+NIRS single-trial clas- siﬁcation,” IEEE Trans. Neural Syst. Rehabil. Eng., vol. 25, no. 10, pp. 1735–1745, Oct. 

2017. 

[21] J. Shin, J. Kwon, and C.-H. Im, “A ternary hybrid EEG-NIRS brain- computer interface for the classiﬁcation of brain activation patterns during mental arithmetic, motor imagery, and idle state,” Frontiers Neuroinform., vol. 12, p. 5, Feb. 

2018. 

[22] F. Al-Shargie, T. B. Tang, and M. Kiguchi, “Stress assessment based on decision fusion of EEG and fNIRS signals,” IEEE Access, vol. 5, pp. 19889–19896, 

2017. 

[23] L.-W. Ko et al., “Multimodal fuzzy fusion for enhancing the motor- imagery-based brain computer interface,” IEEE Comput. Intell. Mag., vol. 14, no. 1, pp. 96–106, Feb. 

2019. 

[24] C.-H. Han, K.-R. M´’uller, and H.-J. Hwang, “Enhanced performance of a brain switch by simultaneous use of EEG and NIRS data for asyn- chronous brain-computer interface,” IEEE Trans. Neural Syst. Rehabil. Eng., vol. 28, no. 10, pp. 2102–2112, Oct. 

2020. 

[25] X. Jiang, X. Gu, K. Xu, H. Ren, and W. Chen, “Independent decision path fusion for bimodal asynchronous brain–computer inter- face to discriminate multiclass mental states,” IEEE Access, vol. 7, pp. 165303–165317, 

2019. 

[26] S. Fazli, J. Mehnert, J. Steinbrink, and B. Blankertz, “Using NIRS as a predictor for EEG-based BCI performance,” in Proc. Annu. Int. Conf. IEEE Eng. Med. Biol. Soc., Aug. 2012, pp. 4911–

4914. 

[27] H. Morioka et al., “Decoding spatial attention by using cortical currents estimated from electroencephalography with near-infrared spectroscopy prior information,” NeuroImage, vol. 90, pp. 128–139, Apr. 

2014. 

[28] K. Simonyan and A. Zisserman, “Very deep convolutional networks for large-scale image recognition,” 2014, arXiv:

1409.

1556. 

[29] K. Simonyan and A. Zisserman, “Very deep convolutional networks for large-scale image recognition,” 2014, arXiv:

1409.

1556. 

[30] J. Redmon and A. Farhadi, “YOLOv3: An incremental improvement,” 2018, arXiv:

1804.

02767. 

[31] G. Hinton et al., “Deep neural networks for acoustic modeling in speech recognition: The shared views of four research groups,” IEEE Signal Process. Mag., vol. 29, no. 6, pp. 82–97, Nov. 

2012. 

[32] A. M. Chiarelli, P. Croce, A. Merla, and F. Zappasodi, “Deep learning for hybrid EEG-fNIRS brain–computer interface: Application to motor imagery classiﬁcation,” J. Neural Eng., vol. 15, no. 3, Apr. 2018, Art. no. 

036028. 

[33] Z. Sun, Z. Huang, F. Duan, and Y. Liu, “A novel multimodal approach for hybrid brain–computer interface,” IEEE Access, vol. 8, pp. 89909–89918, 

2020. 

[34] Y. Kwak, K. Kong, W.-J. Song, B.-K. Min, and S.-E. Kim, “Multilevel feature fusion with 3D convolutional neural network for EEG-based workload estimation,” IEEE Access, vol. 8, pp. 16009–16021, 

2020. 

[35] X. Zhao, H. Zhang, G. Zhu, F. You, S. Kuang, and L. Sun, “A multi- branch 3D convolutional neural network for EEG-based motor imagery classiﬁcation,” IEEE Trans. Neural Syst. Rehabil. Eng., vol. 27, no. 10, pp. 2164–2177, Oct. 

2019. 

[36] J.-H. Jeong, K.-H. Shim, D.-J. Kim, and S.-W. Lee, “Brain-controlled robotic arm system based on multi-directional CNN-BiLSTM network using EEG signals,” IEEE Trans. Neural Syst. Rehabil. Eng., vol. 28, no. 5, pp. 1226–1238, May 

2020. 

[37] C. G. Snoek, M. Worring, and A. W. Smeulders, “Early versus late fusion in semantic video analysis,” in Proc. 13th Annu. ACM Int. Conf. Multimedia, Nov. 2005, pp. 399–

402. 

[38] N. Neverova, C. Wolf, G. W. Taylor, and F. Nebout, “Multi-scale deep learning for gesture detection and localization,” in Proc. Workshop Eur. Conf. Comput. Vis., Cham, Switzerland: Springer, Sep. 2014, pp. 474–

490. 

[39] V. Vielzeuf, A. Lechervy, S. Pateux, and F. Jurie, “Multilevel sensor fusion with deep learning,” IEEE Sensors Lett., vol. 3, no. 1, pp. 1–4, Jan. 

2019. 

[40] Y.-R. Cho, S. Shin, S.-H. Yim, K. Kong, H.-W. Cho, and W.-J. Song, “Multistage fusion with dissimilarity regularization for SAR/IR target recognition,” IEEE Access, vol. 7, pp. 728–740, 

2019. 

[41] X. Yang, P. Molchanov, and J. Kautz, “Multilayer and multimodal fusion of deep neural networks for video classiﬁcation,” in Proc. ACM Multimedia Conf., Oct. 2016, pp. 978–

987. 

[42] C. S. Roy and C. S. Sherrington, “On the regulation of the blood- supply of the brain,” J. Physiol., vol. 11, nos. 1–2, pp. 85–158, Jan. 

1890. 

[43] P. Lachert, D. Janusek, P. Pulawski, A. Liebert, D. Milej, and K. J. Blinowska, “Coupling of Oxy- and deoxyhemoglobin concentra- tions with EEG rhythms during motor task,” Sci. Rep., vol. 7, no. 1, pp. 1–9, Nov. 

2017. 

[44] M. Takeuchi et al., “Brain cortical mapping by simultaneous recording of functional near infrared spectroscopy and electroencephalograms from the whole brain during right median nerve stimulation,” Brain Topography, vol. 22, no. 3, pp. 197–214, Aug. 

2009. 

[45] A. Gundel and G. F. Wilson, “Topographical changes in the ongoing EEG related to the difﬁculty of mental tasks,” Brain Topography, vol. 5, no. 1, pp. 17–25, 

1992. 

[46] M. Benedek, R. J. Schickel, E. Jauk, A. Fink, and A. C. Neubauer, “Alpha power increases in right parietal cortex reﬂects focused internal attention,” Neuropsychologia, vol. 56, pp. 393–400, Apr. 

2014. 

[47] L. Brinkman, A. Stolk, H. C. Dijkerman, F. P. de Lange, and I. Toni, “Distinct roles for Alpha- and beta-band oscillations during mental simulation of goal-directed actions,” J. Neurosci., vol. 34, no. 44, pp. 14783–14792, Oct. 

2014. 

[48] L. Kocsis, P. Herman, and A. Eke, “The modiﬁed beer–lambert law revisited,” Phys. Med. Biol., vol. 51, no. 5, pp. N91–N98, Mar. 

2006. 

[49] D. Tran, L. Bourdev, R. Fergus, L. Torresani, and M. Paluri, “Learning spatiotemporal features with 3D convolutional networks,” in Proc. IEEE Int. Conf. Comput. Vis., Dec. 2015, pp. 4489–

4497. 

[50] S. Ji, W. Xu, M. Yang, and K. Yu, “3D convolutional neural networks for human action recognition,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 35, no. 1, pp. 221–231, Jan. 

2012. 

[51] N. Srivastava, G. Hinton, A. Krizhevsky, I. Sutskever, and R. Salakhut- dinov, “Dropout: A simple way to prevent neural networks from over- ﬁtting,” J. Mach. Learn. Res., vol. 15, no. 1, pp. 1929–1958, Jan. 

2014. 

[52] O. Jensen, J. Gelfand, J. Kounios, and J. E. Lisman, “Oscillations in the alpha band (9–12 Hz) increase with memory load during retention in a short-term memory task,” Cerebral Cortex, vol. 12, no. 8, pp. 877–882, 

2002. 

[53] D. P. Kingma and J. Ba, “Adam: A method for stochastic optimization,” 2014, arXiv:

1412.

6980. 

[54] E. Ergün and O. Aydemir, “A new evolutionary preprocessing approach for classiﬁcation of mental arithmetic based EEG signals,” Cognit. Neurodyn., vol. 14, no. 5, pp. 609–617, Apr. 

2020. 

[55] E. Ergün and O. Aydemir, “Decoding of binary mental arithmetic based near-infrared spectroscopy signals,” in Proc. 3rd Int. Conf. Comput. Sci. Eng. (UBMK), Sep. 2018, pp. 201–

204. 

[56] E. Ergun and O. Aydemir, “Classiﬁcation of motor imaginary based near- infrared spectroscopy signals,” in Proc. 26th Signal Process. Commun. Appl. Conf. (SIU), May 2018, pp. 1–

4. 

[57] E. A. Aydin, “Subject-speciﬁc feature selection for near infrared spec- troscopy based brain-computer interfaces,” Comput. Methods Programs Biomed., vol. 195, Oct. 2020, Art. no. 

105535.