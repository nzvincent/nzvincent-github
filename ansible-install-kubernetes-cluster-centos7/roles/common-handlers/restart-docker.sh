---

- handlers:

  - name: Restart Docker
    shell: 
      servie docker restart
    register: command_output
    
    
