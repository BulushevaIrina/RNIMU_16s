#conda activate qiime2-2020.2

#1# make manifest file

#2# import manifest file with the following command
qiime tools import \
     --type 'SampleData[PairedEndSequencesWithQuality]' \
     --input-path manifest.txt \
     --output-path UMtutorial-demux-paired-end.qza \
     --input-format PairedEndFastqManifestPhred33
#3# high-level summary of your sequence quality using the qiime demux summarize command

qiime demux summarize  \
     --i-data UMtutorial-demux-paired-end.qza  \
     --o-visualization UMtutorial-demux-paired-end.qzv  \
     --p-n 100000


qiime cutadapt trim-paired \
     --i-demultiplexed-sequences UMtutorial-demux-paired-end.qza \
     --p-cores 8 \
     --p-front-f GTGYCAGCMGCCGCGGTAA \
     --p-front-r GGACTACNVGGGTWTCTAAT \
     --verbose \
     --o-trimmed-sequences UMtrimmed_sequences.qza

qiime vsearch join-pairs \
     --i-demultiplexed-seqs UMtrimmed_sequences.qza \
     --p-minovlen 5 \
     --p-maxdiffs 20 \
     --p-threads 8 \
     --verbose \
     --o-joined-sequences UMdemux-joined.qza


qiime deblur denoise-16S \
     --i-demultiplexed-seqs UMdemux-joined.qza \
     --p-trim-length 240 \
     --p-jobs-to-start 8 \
     --p-sample-stats \
     --o-representative-sequences UMrep-seqs-deblur.qza \
     --o-table UMtable-deblur.qza \
     --o-stats UMdeblur-stats.qza

#qiime tools validate demux.qza



qiime feature-table tabulate-seqs \
     --i-data UMrep-seqs-deblur.qza \
     --o-visualization UMrep-seqsO.qzv

#feature frequency
qiime feature-table summarize \
   --i-table UMtable-deblur.qza \
   --o-visualization UM-exp.qzv

qiime tools export \
  --input-path UM-exp.qzv \
  --output-path feature_frequency

qiime tools export \
  --input-path UMrep-seqsO.qzv \
  --output-path feature_sequences




