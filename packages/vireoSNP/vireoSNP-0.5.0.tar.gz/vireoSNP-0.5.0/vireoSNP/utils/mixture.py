


    def update_theta_size(self, AD, DP):
        """Coordinate ascent for updating theta posterior parameters
        """
        BD = DP - AD
        S1_gt = AD @ self.ID_prob  #(n_var, n_donor)
        S2_gt = BD @ self.ID_prob  #(n_var, n_donor)
        
        _theta_s1 = np.zeros(self.beta_mu.shape)
        _theta_s2 = np.zeros(self.beta_mu.shape)
        _theta_s1 += self.theta_s1_prior.copy()
        _theta_s2 += self.theta_s2_prior.copy()
        for ig in range(self.n_GT):
            _axis = 1 if self.ASE_mode else None
            _theta_s1[:, ig:(ig+1)] += np.sum(
                S1_gt * self.GT_prob[:, :, ig], axis=_axis, keepdims=True)
            _theta_s2[:, ig:(ig+1)] += np.sum(
                S2_gt * self.GT_prob[:, :, ig], axis=_axis, keepdims=True)
        
        self.beta_mu = _theta_s1 / (_theta_s1 + _theta_s2)
        if self.fix_beta_sum == False:
            self.beta_sum = _theta_s1 + _theta_s2
            
        # ## add new implementation: share GT=0 and 2
        # self.beta_sum[:, 0] = (_theta_s1[:, [0, 2]] + _theta_s2[:, [0, 2]]).sum()
        # self.beta_sum[:, 2] = (_theta_s1[:, [0, 2]] + _theta_s2[:, [0, 2]]).sum()
        # self.beta_mu[:, 0] = (_theta_s1[:, 0] + _theta_s2[:, 2]).sum() / self.beta_sum[:, 0]
        # self.beta_mu[:, 2] = 1 - self.beta_mu[:, 0]

        # # self.beta_mu[:, 0] = 0.00001
        # # self.beta_mu[:, 2] = 0.00001
        # # self.beta_sum[:, 0] = 10000000
        # # self.beta_sum[:, 2] = 10000000