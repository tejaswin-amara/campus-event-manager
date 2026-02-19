package com.tejaswin.campus.service;

import com.tejaswin.campus.model.User;
import com.tejaswin.campus.repository.UserRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class UserService {

    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Transactional(readOnly = true)
    public User authenticate(String username, String password) {
        User user = userRepository.findByUsername(username).orElse(null);
        if (user != null && user.getPassword() != null && user.getPassword().equals(password)) {
            return user;
        }
        return null;
    }

    @Transactional(readOnly = true)
    public User getGuestUser() {
        return userRepository.findByUsername("guest").orElse(null);
    }
}
