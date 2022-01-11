#!/bin/bash
set -e

declare -A settings
name="leds"
currentDir=$(pwd)
configFile="$(pwd)/web/config/install.cfg"
configurationString=""

helpPrint()
{
    echo ""
    echo "Usage: $0 [-i][-r][-u][-h]"
    echo -e "\t-i pin=18,port=9000,ledCount=100:pin=21,port=9001,ledCount=30"
    echo -e "\t   Installs service with the provided configuration or reinstalls if .install.cfg already exists"
    echo -e "\t-r \n\t   Reinstalls current installation."
    echo -e "\t-u \n\t   Uninstall current installation."
    echo -e "\t-h \n\t   Display this help message"
    exit 1 # Exit script after printing help
}

requireRoot()
{
    if [ "$(id -u)" -ne "0" ] ; then
        echo "This script must be executed with root privileges."
        exit 1
    fi
}

installDocker()
{
    if [ ! -x "$(command -v docker)" ]
    then
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        rm get-docker.sh
    fi
}

parseCommands()
{
    instances=0
    configurations=$1
    readarray -d ":" -t configArray <<<"$configurations"
    for instanceCfgs in "${configArray[@]}"
    do
        instances=$((instances+1))
        readarray -d "," -t instanceArgs <<<"$instanceCfgs"

        for configs in "${instanceArgs[@]}"
        do
            readarray -d "=" -t configPair <<<"$configs"

            if [ ${#configPair[@]} != 2 ]; 
            then
                echo "Invalid key value pair, should be: key=value"
                exit 1
            fi
            
            key=${configPair[0]//$'\n'/}
            value=${configPair[1]//$'\n'/}

            if [ $key == "pin" ] || [ $key == "port" ] || [ $key == "ledCount" ]; 
            then
                if ! [[ $value =~ ^[0-9]+([.][0-9]+)?$ ]];
                then
                    echo "Invalid value provided, shoud be number!"
                    exit 1
                else
                    settings["${instances}-${key}"]+=$value
                fi
            else
                echo "Only \"pin\", \"port\" and \"ledCount\" keys are supported"
                exit 1
            fi
        done
    done
}

getInstallConfig()
{
    configString=""
    if test -f "$configFile"
    then
        configString="$(cat ${configFile})"
    fi

    if [ "$1" == "reinstall" ] && [ -z "$configString" ]
    then
        echo "Error: .install.cfg does not exist - nothing to reinstall"
        exit 1
    elif [ -n "$configString" ] && [ -n "$configurationString" ]
    then
        echo "Error: .install.cfg exists. Uninstall with: \"$0 -u\" or delete the file manually."
        exit 1
    elif [ "$1" == "uninstall" ]
    then
        echo "Uninstalling.."
    elif [ -n "$configString" ]
    then
        echo ".install.cfg exists -> reinstalling existing installation with ${configString}."
        configurationString=$configString
    fi
}

createDockerNetwork()
{
    if [[ "$(docker network ls | grep ${name}-network)" == "" ]]
    then
        docker network create --driver bridge ${name}-network
    fi
}

installDockerContainers()
{
    sudo systemctl reset-failed
    for (( instance=1; instance <= $instances; ++instance ))
    do
        containerName="${name}-${instance}"
        pin=${settings["${instance}-pin"]}
        port=${settings["${instance}-port"]}
        ledCount=${settings["${instance}-ledCount"]}

        if systemctl --all --type service | grep -q "${name}-${instance}.service"
        then
            echo "Stopping & disabling service: ${name}-${instance}.service..."
            sudo systemctl stop ${name}-${instance}.service
            sudo systemctl disable ${name}-${instance}.service
        fi
        
        if [ "$(docker ps -a | grep ${name}-${instance})" ]
        then
            echo "Deleting container: ${name}-${instance}..."
            docker rm ${name}-${instance}
        fi

        echo "Building image: gradrix/${name}-${instance}..."
        sudo docker build -t gradrix/${name}-${instance} --build-arg pin=${pin} --build-arg port=${port} --build-arg ledCount=${ledCount} -f ./docker/gpio-service/Dockerfile .

        echo "Creating and running cointainer once..."
        docker run --name ${name}-${instance} -it --device /dev/gpiomem -p ${port}:${port} --privileged -d --restart unless-stopped --network ${name}-network gradrix/${name}-${instance}
    
        echo "Stopping container..."
        docker stop ${name}-${instance}

        installService ${name}-${instance} ${name}
    done

    echo "Building web images"
    docker-compose build --force-rm --parallel

    installWebService "${name}-web"
}

installWebService()
{
    service=$1

cat << EOF | sudo tee /lib/systemd/system/${service}.service
[Unit]
Description=Leds-Web Service
After=network.target docker.service

[Service]
WorkingDirectory=$currentDir
Type=simple
Restart=always
ExecStart=/usr/local/bin/docker-compose up --remove-orphans
ExecStop=/usr/local/bin/docker-compose down --remove-orphans

[Install]
WantedBy=multi-user.target
EOF
    startAndEnableService $service
}

installService()
{
    service=$1

    echo "Adding ${service}.service file to systemd..."
    cat << EOF | sudo tee /lib/systemd/system/${service}.service
[Unit]
Description=${service} service
Requires=docker.service
After=docker.service

[Service]
Restart=always
ExecStart=docker start -a ${service}
ExecStop=docker stop -t 2 ${service}

[Install]
WantedBy=default.target
EOF
    startAndEnableService $service
}

startAndEnableService()
{
    service=$1

    echo "Reloading systemd daemon..."
    sudo systemctl daemon-reload

    echo "Enabling ${service}.service"
    sudo systemctl enable ${service}.service

    echo "Starting ${service}.service"
    sudo systemctl start ${service}.service

    sleep 1

    if systemctl --state=failed --type service | grep -q "${service}.service"
    then
        echo "Service ${service}.service failed to start.."
        sudo systemctl status ${service}.service
        exit 1
    fi
}

install()
{
    mkdir -p frontend-build
    sudo chmod -R a+rwx frontend-build

    getInstallConfig $1
    parseCommands $configurationString

    #requireRoot
    installDocker
    
    createDockerNetwork
    installDockerContainers

    saveConfig
}

uninstall()
{
    removeConfigs
    removeContainers
    exit 1
}

removeConfigs()
{
    getInstallConfig "uninstall"

    if ! [ -z "$instances" ]; 
    then
        for (( instance=1; instance <= $instances; ++instance ))
        do
            containerName="${name}-${instance}"

            if systemctl --all --type service | grep -q "${name}-${instance}.service"
            then
                echo "Stopping, disabling and removing service: ${name}-${instance}.service..."
                sudo systemctl stop ${name}-${instance}.service || true
                sudo systemctl disable ${name}-${instance}.service || true
                sudo rm /lib/systemd/system/${name}-${instance}.service || true
            fi
        done
    fi

    sudo systemctl stop ${name}-web.service || true
    sudo systemctl disable ${name}-web.service || true
    sudo rm /lib/systemd/system/${name}-web.service || true
    sudo systemctl daemon-reload
    sudo systemctl reset-failed

    rm -rf ${configFile} || true
}

removeContainers()
{
    echo "Removing docker containers..."
    if [ -z "$(docker ps -a | grep gradrix)" ]; 
    then 
        echo "Nothing to remove.";
    else
        docker ps -a | grep gradrix | awk '{print $1}' | xargs docker stop | xargs docker rm
        echo "Done."
    fi 

    echo "Removing docker images..."
    if [ -z "$(docker images -a | grep gradrix)" ];
    then
        echo "Nothing to remove.";
    else
        docker images -a | grep gradrix | awk '{print $1}' | xargs docker image rm
    fi
}

saveConfig()
{
    echo "Saving install config..."
    echo "$configurationString" | tee ${configFile}
}

checkIfParametersProvided()
{
    # Print helpFunction in case parameters are empty
    if [ -z "$configurationString" ] && [ "$opt" != "u" ]
    then
        echo "Configurations were not provided!";
        helpPrint
    fi
}

handleCliCommands()
{   
    if [ $# -eq 0 ]; then
        helpPrint
        exit 1
    fi
    while getopts "i:ruh:" opt
    do
        case "$opt" in
            i ) 
                configurationString="$OPTARG" 
                install ;;
            r )
                install "reinstall" ;;
            u )
                uninstall ;;
            h ) helpPrint ;; # Print helpFunction in case parameter is non-existent
        esac
    done
}

handleCliCommands "$@"
