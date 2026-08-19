package com.tejaswin.campus.repository;

import com.tejaswin.campus.model.Registration;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import org.springframework.data.repository.query.Param;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Repository
public interface RegistrationRepository extends JpaRepository<Registration, Long> {

    boolean existsByUserIdAndEventId(Long userId, Long eventId);

    @Query("SELECT r FROM Registration r JOIN FETCH r.event WHERE r.user.id = :userId ORDER BY r.registrationDate DESC")
    List<Registration> findByUserIdWithEvent(@Param("userId") Long userId);

    long countByEventId(Long eventId);

    @Transactional
    void deleteByEventId(Long eventId);

    @Query("SELECT r.event.id, COUNT(r) FROM Registration r GROUP BY r.event.id")
    List<Object[]> countRegistrationsGroupedByEvent();

}
