#conda activate qiime2-2020.2

#1# make manifest file

#2# import manifest file with the following command
qiime tools import \
     --type 'SampleData[SequencesWithQuality]' \
     --input-path manifest_SE.txt \
     --output-path UMtutorial-demux-single-end.qza \
     --input-format SingleEndFastqManifestPhred33


#3# high-level summary of your sequence quality using the qiime demux summarize command

qiime demux summarize  \
     --i-data UMtutorial-demux-single-end.qza  \
     --o-visualization UMtutorial-demux-single-end.qzv  \
     --p-n 100000
#produce a QIIME visualization of your data quality and tabular summary of the sequences in your dataset, which you can view by dragging and dropping it at the q2view website: https://view.qiime2.org/


#4# DADA2 module in QIIME to denoise your sequences into amplicon sequence variants (ASVs) or operational taxonomic units (OTUs)

qiime dada2 denoise-single \
     --i-demultiplexed-seqs UMtutorial-demux-single-end.qza \
     --p-trim-left 28 \
     --p-trunc-len 0 \
     --p-n-threads 8 \
     --o-representative-sequences UMrep-seqs-dada2O \
     --o-table UMtable-dada2O \
     --o-denoising-stats UMdenoising-stats.qza

qiime feature-table tabulate-seqs \
     --i-data UMrep-seqs-dada2O.qza \
     --o-visualization UMrep-seqsO.qzv

#feature frequency
qiime feature-table summarize \
   --i-table UMtable-dada2O.qza \
   --o-visualization UM-exp.qzv

qiime tools export \
  --input-path UM-exp.qzv \
  --output-path feature_frequency

qiime tools export \
  --input-path UMrep-seqsO.qzv \
  --output-path feature_sequences



