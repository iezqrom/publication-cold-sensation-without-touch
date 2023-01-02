function [RF] = quest_matlab_set_up(alphas)
   alphas = cell2mat(alphas);
   RF = PAL_AMRF_setupRF;
   RF = PAL_AMRF_setupRF(RF, 'priorAlphaRange', alphas);
end